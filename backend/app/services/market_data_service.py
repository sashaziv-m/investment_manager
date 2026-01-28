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
                "momentum_score": round(float(current_momentum), 2)
            }
        except Exception as e:
            logger.error(f"Error calculating momentum for {symbol}: {e}")
            return None

    @staticmethod
    def check_alpha_vantage_key():
        if settings.ALPHA_VANTAGE_API_KEY:
            return True
        return False
