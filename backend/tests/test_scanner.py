import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from app.services.market_data_service import MarketDataService

def test_calculate_momentum():
    with patch("app.services.market_data_service.yf.Ticker") as mock_ticker:
        mock_instance = mock_ticker.return_value
        
        # Create mock data: 201 days of rising price
        prices = [100 + i for i in range(201)]
        df = pd.DataFrame({"Close": prices})
        mock_instance.history.return_value = df
        
        result = MarketDataService.calculate_momentum("TEST")
        
        assert result is not None
        assert result['symbol'] == "TEST"
        assert result['price'] == 300.0 # 100 + 200
        # Positive momentum
        assert result['momentum_score'] > 0
        # RSI should be high (100 or close) because straight line up
        assert result['rsi_14'] > 90
        # SMA 50 should be lower than SMA 200 ??? No, with rising price: Price > SMA50 > SMA200
        assert result['sma_50'] > result['sma_200']
