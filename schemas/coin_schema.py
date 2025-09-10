from pydantic import BaseModel

class CoinCreate(BaseModel):
    symbol: str
    name: str

class CoinResponse(BaseModel):
    symbol: str
    name: str

class CoinResponse1(BaseModel):
    id : int
    symbol: str
    name: str