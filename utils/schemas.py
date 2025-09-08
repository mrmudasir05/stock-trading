from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from typing import Annotated


class WalletResponse(BaseModel):
    coin_id: int
    balance: float
    coins : int
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class RechargeResponse(BaseModel):
    username:str
    balance:float
    class Config:
        orm_mode = True

class TradeResponse(BaseModel):
    coin_id: int
    trade_type: str
    quantity: float
    price: float
    created_at: datetime
    class Config:
        orm_mode = True

class CoinResponse(BaseModel):
    symbol: str
    name: str

class CoinResponse1(BaseModel):
    id : int
    symbol: str
    name: str

# ---------- User ----------
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

# ---------- Balance ----------
class BalanceRecharge(BaseModel):
    amount: Annotated[float, Field(..., gt=0)]

# ---------- Coin ----------
class CoinCreate(BaseModel):
    symbol: str
    name: str

# ---------- Transaction ----------
class TransactionCreate(BaseModel):
    wallet_id: int
    amount: Annotated[float, Field(..., gt=0)]

# ---------- Trade ----------
class TradeCreate(BaseModel):
    coin_id: Annotated[int, Field(..., gt=0)]
    quantity: Annotated[int, Field(..., gt=0)]
    price: Annotated[float, Field(..., gt=0)]
