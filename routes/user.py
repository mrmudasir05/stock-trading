from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from schemas import user_schema
from utils.security import get_current_user, get_db
from utils import operations

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/info", response_model=user_schema.UserMe)
async def get_user_info(current_user: models.User = Depends(get_current_user)):
    """

    :param current_user: logged in user
    :return: current user
    """
    return current_user


@router.get("/wallets", response_model=user_schema.UserWallets)
async def get_user_wallets(current_user: models.User = Depends(get_current_user)) -> dict:
    """

    :param current_user: logged in user
    :return: wallets for current user
    """
    return {"wallets": current_user.wallets}


@router.get("/trades", response_model=user_schema.UserTrade)
async def get_user_trades(current_user: models.User = Depends(get_current_user)):
    """

        :param current_user: logged in user
        :return: trades for current user
        """
    return {"trades": current_user.trades}


@router.put("/update", response_model=user_schema.UserInfo)
async def update_user(
    user_update: user_schema.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """

    :param user_update: user update schema
    :param db: session for the database
    :param current_user: logged in user
    :return: updates the entered data for user in database
    """
    return operations.update_user(db, current_user.id, user_update)


@router.delete("/me")
async def delete_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """

    :param db: session of the database
    :param current_user: logged in user
    :return: delete the user from the database
    """
    return operations.delete_user(db, current_user.id)


@router.post("/recharge", response_model=user_schema.RechargeResponse)
async def recharge_balance(
    recharge: user_schema.BalanceRecharge,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """

    :param recharge: Balance recharge schema
    :param db: session of the database
    :param current_user: logged in user
    :return: add the entered balance in the current user balance
    """
    if recharge.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    user = operations.add_balance(db, current_user.id, recharge.amount)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/all_users", response_model=list[user_schema.UserInfo])
async def get_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """

    :param db: session of the database
    :param current_user: logged in user
    :return: list of all users with basic information
    """
    users = db.query(models.User).all()
    return users