from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from typing import Annotated
from schemas.trade_schema import TradeResponse
from schemas.wallet_schema import WalletResponse

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    id: int
    username: str
    email: str

class UserMe(BaseModel):
    id: int
    username: str
    email: str
    balance : Annotated[float, Field(..., ge=0)]


class UserTrade(BaseModel):
    trades: List[TradeResponse] = []
    class Config:
        orm_mode = True

class UserWallets(BaseModel):
    wallets: List[WalletResponse] = []
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    class Config:
        orm_mode = True



class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class BalanceRecharge(BaseModel):
    amount: Annotated[float, Field(..., gt=0)]

class RechargeResponse(BaseModel):
    username:str
    balance:float
    class Config:
        orm_mode = True