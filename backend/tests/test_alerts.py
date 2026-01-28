import pytest
from unittest.mock import patch
from app.services.notification_service import NotificationService
from app.worker.tasks import check_alerts
from app.core.config import settings

def test_send_alert():
    with patch("app.services.notification_service.logger") as mock_logger:
        NotificationService.send_alert("Test Alert", "admin@test.com")
        mock_logger.info.assert_called_with("ALERT SENT to admin@test.com: Test Alert")

@pytest.mark.asyncio
async def test_check_alerts_trigger():
    # Test that check_alerts calls send_alert when threshold is breached
    with patch("app.worker.tasks.yf.Ticker") as mock_ticker:
        mock_instance = mock_ticker.return_value
        import pandas as pd
        # Mock VIX at 30.0 (Crisis)
        mock_instance.history.return_value = pd.DataFrame({"Close": [30.0]})
        
        with patch("app.services.notification_service.NotificationService.send_alert") as mock_send:
            check_alerts() # Synchronous call for testing
            mock_send.assert_called()
            args, _ = mock_send.call_args
            assert "CRISIS" in args[0]
