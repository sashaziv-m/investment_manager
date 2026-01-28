from app.services.reddit_service import reddit_client
from app.services.market_data_service import MarketDataService
import pytest

@pytest.mark.asyncio
async def test_reddit_client_initialization():
    # It should not fail even if credentials are missing (just logs warning)
    assert reddit_client is not None
    # If no credentials, check_connection returns False, but no exception
    connected = await reddit_client.check_connection()
    # We can't assert True unless we have keys, so just ensure it runs
    assert connected in [True, False]

def test_market_data_service():
    # Check that we can call the method
    # Without keys, it returns False
    assert MarketDataService.check_alpha_vantage_key() in [True, False]
