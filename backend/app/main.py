from fastapi import FastAPI, APIRouter
from app.core.config import settings
from app.services.vix_service import get_current_vix

app = FastAPI(title=settings.PROJECT_NAME)

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

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Investment App API"}
