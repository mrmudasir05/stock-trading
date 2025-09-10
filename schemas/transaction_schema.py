from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from typing import Annotated

class TransactionCreate(BaseModel):
    wallet_id: int
    amount: Annotated[float, Field(..., gt=0)]