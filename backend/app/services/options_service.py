import logging
import yfinance as yf
from typing import List, Dict

logger = logging.getLogger(__name__)

class OptionsService:
    async def get_unusual_activity(self, tickers: List[str] = ["SPY", "QQQ", "TSLA", "NVDA", "AMD", "AAPL"]) -> List[Dict]:
        """
        Scans for high volume options chains.
        Note: Real-time options flow is expensive. This uses delayed data via yfinance
        to find "Unusual" volume (Volume > Open Interest).
        """
        activity = []
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                # Get earliest expiration
                expirations = stock.options
                if not expirations:
                    continue
                
                # Check closest expiration (weekly activity)
                chain = stock.option_chain(expirations[0])
                
                # Filter Calls
                calls = chain.calls
                # Volume > 500 and Volume > OpenInterest (Signal of aggressive opening)
                unusual_calls = calls[(calls['volume'] > 500) & (calls['volume'] > calls['openInterest'])]
                
                for _, row in unusual_calls.iterrows():
                    activity.append({
                        "symbol": ticker,
                        "type": "Call",
                        "strike": row['strike'],
                        "expiration": expirations[0],
                        "volume": int(row['volume']),
                        "open_interest": int(row['openInterest']),
                        "vol_oi_ratio": round(row['volume'] / (row['openInterest'] or 1), 1),
                        "last_price": row['lastPrice']
                    })

                # Filter Puts
                puts = chain.puts
                unusual_puts = puts[(puts['volume'] > 500) & (puts['volume'] > puts['openInterest'])]
                
                for _, row in unusual_puts.iterrows():
                    activity.append({
                        "symbol": ticker,
                        "type": "Put",
                        "strike": row['strike'],
                        "expiration": expirations[0],
                        "volume": int(row['volume']),
                        "open_interest": int(row['openInterest']),
                        "vol_oi_ratio": round(row['volume'] / (row['openInterest'] or 1), 1),
                        "last_price": row['lastPrice']
                    })
                    
            except Exception as e:
                logger.error(f"Error fetching options for {ticker}: {e}")
                
        # Sort by Volume desc
        activity.sort(key=lambda x: x['volume'], reverse=True)
        return activity[:20]
