import pytest
from unittest.mock import MagicMock, patch
from app.services.vix_service import calculate_vix_status, get_current_vix
from app.core.config import settings

def test_calculate_vix_status():
    # Test Normal
    assert calculate_vix_status(17.9) == "Normal"
    # Test Caution
    assert calculate_vix_status(18.0) == "Caution"
    assert calculate_vix_status(24.9) == "Caution"
    # Test Crisis
    assert calculate_vix_status(25.0) == "Crisis"
    assert calculate_vix_status(30.0) == "Crisis"

@pytest.mark.asyncio
async def test_get_current_vix_success():
    with patch("app.services.vix_service.yf.Ticker") as mock_ticker:
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        
        # Mock history dataframe
        import pandas as pd
        mock_df = pd.DataFrame({"Close": [20.0]})
        mock_instance.history.return_value = mock_df
        
        result = await get_current_vix()
        assert result is not None
        assert result["price"] == 20.0
        assert result["status"] == "Caution"
        assert result["thresholds"]["caution"] == settings.VIX_THRESHOLD_CAUTION

@pytest.mark.asyncio
async def test_get_current_vix_empty():
    with patch("app.services.vix_service.yf.Ticker") as mock_ticker:
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        
        import pandas as pd
        mock_instance.history.return_value = pd.DataFrame()
        
        result = await get_current_vix()
        assert result is None
