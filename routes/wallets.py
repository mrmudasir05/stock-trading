from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from utils.security import get_db
from utils import operations
import models
from utils.security import get_current_user
from schemas import transaction_schema, wallet_schema


router = APIRouter(prefix="/wallets", tags=["Wallet"])


@router.post("/create", response_model=wallet_schema.WalletResponse)
def create(
    request: wallet_schema.WalletCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return operations.wallet_create(db, current_user.id, request.coin_id)


@router.post("/deposit", response_model=wallet_schema.WalletResponse)
def deposit(
    request: transaction_schema.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return operations.deposit_wallet(db, current_user.id, request.wallet_id, request.amount)


@router.post("/withdraw", response_model=wallet_schema.WalletResponse)
def withdraw(
    request: transaction_schema.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return operations.withdraw_wallet(db, current_user.id, request.wallet_id, request.amount)
