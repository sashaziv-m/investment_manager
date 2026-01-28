import yfinance as yf
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class MarketDataService:
    @staticmethod
    async def get_momentum_data(symbol: str, period: str = "1mo"):
        """
        Fetch historical data to calculate momentum.
        Using yfinance for MVP as it's free.
        """
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period)
            if history.empty:
                return None
            return history
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return None

    @staticmethod
    def check_alpha_vantage_key():
        if settings.ALPHA_VANTAGE_API_KEY:
            return True
        return False
