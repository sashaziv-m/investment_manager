from app.core.celery_app import celery_app
from app.services.notification_service import NotificationService
# from app.db.database import SessionLocal # We need a sync session for Celery usually, or handling async properly
import asyncio
from app.services.vix_service import get_current_vix
from app.core.config import settings
import yfinance as yf

# Dealing with async in Celery can be tricky.
# For MVP, we'll do a simple synchronous check or run async loop 

@celery_app.task
def test_task(word: str):
    return f"test task return {word}"

@celery_app.task
def check_alerts():
    """
    Periodic task to check conditions.
    For MVP, we specifically check VIX against thresholds defined in ENV or DB.
    """
    # Create event loop for async calls if needed, or use synchronous library equivalents
    # For VIX, we used yfinance which is synchronous primarily but wrapped in async in vix_service.
    # We can just call yfinance directly here or re-use logic.
    
    # 1. Check VIX
    try:
        ticker = yf.Ticker("^VIX")
        history = ticker.history(period="1d")
        if not history.empty:
            current_vix = history['Close'].iloc[-1]
            
            # Simple threshold check (Hardcoded or from Config for MVP)
            # In real implementation, query AlertRule table
            
            if current_vix > settings.VIX_THRESHOLD_CRISIS:
                NotificationService.send_alert(
                    f"CRISIS: VIX is {current_vix:.2f} (Threshold: {settings.VIX_THRESHOLD_CRISIS})", 
                    "admin@example.com"
                )
            elif current_vix > settings.VIX_THRESHOLD_CAUTION:
                NotificationService.send_alert(
                    f"CAUTION: VIX is {current_vix:.2f} (Threshold: {settings.VIX_THRESHOLD_CAUTION})", 
                    "admin@example.com"
                )
            
    except Exception as e:
        print(f"Error in check_alerts: {e}")
        
    return "Checked Alerts"
