from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.vix_service import get_current_vix
from app.services.portfolio_service import PortfolioService
from app.db.database import get_db
from app import schemas

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

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Investment App API"}
