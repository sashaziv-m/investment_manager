import httpx
from bs4 import BeautifulSoup
import logging
import datetime

logger = logging.getLogger(__name__)

class InsiderTradeService:
    async def get_recent_trades(self, limit=20):
        url = "http://www.openinsider.com/latest-insider-trading"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                html = response.text
                
            soup = BeautifulSoup(html, 'html.parser')
            trades = []
            
            table = soup.find('table', {'class': 'tinytable'})
            if not table:
                logger.error("Could not find table with class 'tinytable' on OpenInsider")
                return []

            rows = table.find_all('tr')
            # Skip header row
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) < 13:
                    continue
                
                # Column mapping for latest-insider-trading:
                # 0: X
                # 1: Filing Date
                # 2: Trade Date
                # 3: Ticker
                # 4: Company Name
                # 5: Insider Name
                # 6: Title
                # 7: Trade Type
                # 8: Price
                # 9: Qty
                # 10: Owned
                # 11: dOwn
                # 12: Value

                date_str = cols[1].text.strip() # Filing Date (more recent usually) or Trade Date (col 2). Let's use Filing Date for "Just Released" vibe.
                trade_date = cols[2].text.strip()
                ticker = cols[3].text.strip()
                insider_name = cols[5].text.strip()
                title = cols[6].text.strip()
                trade_type = cols[7].text.strip()
                value_str = cols[12].text.strip()
                
                # Cleanup Value (remove + and $)
                # Frontend expects string is fine, but cleaner is better.
                # Actually frontend handles raw string display if not number.
                
                trades.append({
                    "symbol": ticker,
                    "insider": insider_name,
                    "relation": title,
                    "trade_type": trade_type,
                    "price": 0,
                    "quantity": 0,
                    "value": value_str,
                    "date": date_str
                })

            return trades[:limit]

        except Exception as e:
            logger.error(f"Error scraping OpenInsider: {e}")
            return []

        except Exception as e:
            logger.error(f"Error scraping OpenInsider: {e}")
            return []
