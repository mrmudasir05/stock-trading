from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from utils.security import get_db
from utils import operations
import models
from utils.security import get_current_user
from schemas import transaction_schema, wallet_schema


router = APIRouter(prefix="/wallets", tags=["Wallet"])


@router.post("/create", response_model=wallet_schema.WalletResponse)
async def create(
    request: wallet_schema.WalletCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> wallet_schema.WalletResponse:
    """

    :param request: Wallet create schema
    :param db: session of the database
    :param current_user: logged in user
    :return: create wallet in the wallets table
    """
    return operations.wallet_create(db, current_user.id, request.coin_id)


@router.post("/deposit", response_model=wallet_schema.WalletResponse)
async def deposit(
    request: transaction_schema.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> wallet_schema.WalletResponse:
    """

        :param request: Transaction create schema
        :param db: session of the database
        :param current_user: logged in user
        :return: deposit money in the wallets on wallet ID
        """
    return operations.deposit_wallet(db, current_user.id, request.wallet_id, request.amount)


@router.post("/withdraw", response_model=wallet_schema.WalletResponse)
async def withdraw(
    request: transaction_schema.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> wallet_schema.WalletResponse:
    """

            :param request: Transaction create schema
            :param db: session of the database
            :param current_user: logged in user
            :return: withdraw money from the wallets on wallet ID
            """
    return operations.withdraw_wallet(db, current_user.id, request.wallet_id, request.amount)
