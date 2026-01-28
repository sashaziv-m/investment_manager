from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.vix_service import get_current_vix
from app.services.portfolio_service import PortfolioService
from app.db.database import get_db
from app import schemas

from app.services.market_data_service import MarketDataService
from typing import List
from pydantic import BaseModel

app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

@api_router.get("/vix")
async def read_vix():
    vix_data = await get_current_vix()
    if vix_data:
        return vix_data
    return {"error": "Could not fetch VIX data"}

@api_router.get("/portfolio/holdings", response_model=list[schemas.Holding])
async def get_holdings(db: AsyncSession = Depends(get_db)):
    service = PortfolioService(db)
    return await service.get_holdings()

@api_router.post("/portfolio/holdings", response_model=schemas.Holding)
async def add_holding(holding: schemas.HoldingCreate, db: AsyncSession = Depends(get_db)):
    service = PortfolioService(db)
    return await service.add_holding(holding)

# Scanner Endpoints
class ScanRequest(BaseModel):
    symbols: List[str] = ["AAPL", "MSFT", "NVDA", "TSLA", "AMD", "GOOGL", "AMZN", "META"]

@api_router.post("/scanner/run", tags=["scanner"])
async def run_scan(request: ScanRequest):
    results = []
    for symbol in request.symbols:
        data = MarketDataService.calculate_momentum(symbol)
        if data:
            results.append(data)
    # Sort by momentum score descending
    results.sort(key=lambda x: x['momentum_score'], reverse=True)
    return results

@api_router.get("/social/trends", tags=["social"])
async def get_social_trends():
    from app.services.reddit_service import RedditService
    service = RedditService()
    return await service.get_trends()

@api_router.get("/social/insider-trades", tags=["social"])
async def get_insider_trades():
    from app.services.insider_service import InsiderTradeService
    service = InsiderTradeService()
    return await service.get_recent_trades()

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Investment App API"}
