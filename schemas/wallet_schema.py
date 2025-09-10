from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class WalletCreate(BaseModel):
    coin_id: Annotated[int, Field(..., gt=0)]

class WalletResponse(BaseModel):
    coin_id: int
    balance: float
    coins : int
    class Config:
        orm_mode = True