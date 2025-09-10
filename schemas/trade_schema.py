from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated

class TradeCreate(BaseModel):
    coin_id: Annotated[int, Field(..., gt=0)]
    quantity: Annotated[int, Field(..., gt=0)]
    price: Annotated[float, Field(..., gt=0)]

class TradeResponse(BaseModel):
    coin_id: int
    trade_type: str
    quantity: float
    price: float
    created_at: datetime
    class Config:
        orm_mode = True


