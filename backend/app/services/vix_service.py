import yfinance as yf
import logging

logger = logging.getLogger(__name__)

async def get_current_vix():
    try:
        ticker = yf.Ticker("^VIX")
        # fast_info is often faster for current price
        # but history(period="1d") is more reliable for OHLC
        history = ticker.history(period="1d")
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            return {"symbol": "^VIX", "price": current_price}
        return None
    except Exception as e:
        logger.error(f"Error fetching VIX data: {e}")
        return None
