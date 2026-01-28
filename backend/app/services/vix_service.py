import yfinance as yf
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def calculate_vix_status(price: float) -> str:
    if price >= settings.VIX_THRESHOLD_CRISIS:
        return "Crisis"
    elif price >= settings.VIX_THRESHOLD_CAUTION:
        return "Caution"
    else:
        return "Normal"

async def get_current_vix():
    try:
        ticker = yf.Ticker("^VIX")
        # fast_info is often faster for current price
        # but history(period="1d") is more reliable for OHLC
        history = ticker.history(period="1d")
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            status = calculate_vix_status(current_price)
            return {
                "symbol": "^VIX", 
                "price": current_price,
                "status": status,
                "thresholds": {
                    "caution": settings.VIX_THRESHOLD_CAUTION,
                    "crisis": settings.VIX_THRESHOLD_CRISIS
                }
            }
        return None
    except Exception as e:
        logger.error(f"Error fetching VIX data: {e}")
        return None
