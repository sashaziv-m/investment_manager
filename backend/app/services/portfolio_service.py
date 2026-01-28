from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Holding
from app import schemas
import logging

logger = logging.getLogger(__name__)

class PortfolioService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_holdings(self):
        result = await self.db.execute(select(Holding))
        return result.scalars().all()

    async def add_holding(self, holding: schemas.HoldingCreate):
        db_holding = Holding(
            symbol=holding.symbol.upper(),
            name=holding.name or holding.symbol.upper(),
            quantity=holding.quantity,
            avg_price=holding.avg_price,
            asset_type=holding.asset_type
        )
        self.db.add(db_holding)
        await self.db.commit()
        await self.db.refresh(db_holding)
        return db_holding
