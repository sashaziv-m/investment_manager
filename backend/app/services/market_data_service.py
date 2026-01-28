import yfinance as yf
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class MarketDataService:
    @staticmethod
    def calculate_momentum(symbol: str) -> dict:
        """
        Fetch 1y history and calculate RSI(14), SMA(50), SMA(200), and Momentum (20d).
        """
        try:
            ticker = yf.Ticker(symbol)
            # Fetch enough data for 200 SMA
            hist = ticker.history(period="1y") 
            
            if hist.empty or len(hist) < 200:
                print(f"Not enough data for {symbol}")
                return None

            close = hist['Close']
            
            # Calculate Indicators
            # RSI 14
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # SMA
            sma_50 = close.rolling(window=50).mean()
            sma_200 = close.rolling(window=200).mean()
            
            # Momentum (20d % change)
            momentum_20d = close.pct_change(periods=20) * 100

            current_price = close.iloc[-1]
            current_rsi = rsi.iloc[-1]
            current_sma_50 = sma_50.iloc[-1]
            current_sma_200 = sma_200.iloc[-1]
            current_momentum = momentum_20d.iloc[-1]
            
            return {
                "symbol": symbol,
                "price": round(float(current_price), 2),
                "rsi_14": round(float(current_rsi), 2),
                "sma_50": round(float(current_sma_50), 2),
                "sma_200": round(float(current_sma_200), 2),
            # Golden/Death Cross Detection
            prev_sma_50 = sma_50.iloc[-2]
            prev_sma_200 = sma_200.iloc[-2]
            
            golden_cross = False
            death_cross = False
            
            if prev_sma_50 < prev_sma_200 and current_sma_50 > current_sma_200:
                golden_cross = True
            elif prev_sma_50 > prev_sma_200 and current_sma_50 < current_sma_200:
                death_cross = True

            return {
                "symbol": symbol,
                "price": round(float(current_price), 2),
                "rsi_14": round(float(current_rsi), 2),
                "sma_50": round(float(current_sma_50), 2),
                "sma_200": round(float(current_sma_200), 2),
                "momentum_score": round(float(current_momentum), 2),
                "golden_cross": golden_cross,
                "death_cross": death_cross
            }
        except Exception as e:
            logger.error(f"Error calculating momentum for {symbol}: {e}")
            return None

        if settings.ALPHA_VANTAGE_API_KEY:
            return True
        return False

    async def get_macro_data(self) -> list:
        """
        Fetch key macro indicators: 10y Yield (^TNX), Dollar Index (DX-Y.NYB), VIX (^VIX).
        """
        tickers = ["^TNX", "DX-Y.NYB", "^VIX"]
        data = []
        try:
            for symbol in tickers:
                t = yf.Ticker(symbol)
                # Fast fetch of latest day
                hist = t.history(period="5d")
                if hist.empty:
                    continue
                
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                name = symbol
                if symbol == "^TNX": name = "10Y Yield"
                if symbol == "DX-Y.NYB": name = "Dollar Index"
                if symbol == "^VIX": name = "VIX"

                data.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(current, 2),
                    "change": round(change, 2)
                })
        except Exception as e:
            logger.error(f"Error fetching macro data: {e}")
        
        return data

    async def get_sector_performance(self) -> list:
        """
        Fetch daily performance of major sector ETFs.
        """
        sectors = {
            "XLK": "Technology",
            "XLE": "Energy",
            "XLF": "Financials",
            "XLV": "Healthcare",
            "XLI": "Industrials",
            "XLC": "Comm. Svcs",
            "XLY": "Cons. Disc",
            "XLP": "Cons. Staples"
        }
        data = []
        try:
            for symbol, name in sectors.items():
                t = yf.Ticker(symbol)
                hist = t.history(period="2d")
                if len(hist) < 2:
                    continue
                
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                data.append({
                    "symbol": symbol,
                    "name": name,
                    "price": round(current, 2),
                    "change": round(change, 2)
                })
            
            # Sort by performance
            data.sort(key=lambda x: x['change'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error fetching sector data: {e}")
            
        return data
