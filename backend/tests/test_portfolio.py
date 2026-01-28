import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.portfolio_service import PortfolioService
from app import schemas

@pytest.mark.asyncio
async def test_add_holding():
    mock_db = AsyncMock()
    service = PortfolioService(mock_db)
    
    holding_in = schemas.HoldingCreate(symbol="AAPL", quantity=10, avg_price=150.0)
    
    # Mock data
    # In a real integration test we would use a test DB, but for unit test we mock.
    # However, since add_holding constructs an object we can't easily mock the return of `refresh` 
    # without a lot of sqlalchemy mocking. 
    # So we'll trust the logic flow and assert calls.
    
    await service.add_holding(holding_in)
    
    # Verify add was called
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called

@pytest.mark.asyncio
async def test_get_holdings():
    mock_db = AsyncMock()
    service = PortfolioService(mock_db)
    
    # Mock result
    mock_result = MagicMock()
    # scalars() is synchronous, so we need to set side_effect or configure it to return a MagicMock
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    
    # When result.scalars() is called, return the MagicMock that has .all()
    mock_result.scalars.return_value = mock_scalars
    
    mock_db.execute.return_value = mock_result
    
    holdings = await service.get_holdings()
    assert holdings == []
