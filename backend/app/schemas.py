from pydantic import BaseModel, Field
from typing import Optional

class HoldingBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    quantity: float
    avg_price: float
    asset_type: str = "Stock"

class HoldingCreate(HoldingBase):
    pass

class Holding(HoldingBase):
    id: int
    current_price: Optional[float] = None
    
    class Config:
        from_attributes = True
