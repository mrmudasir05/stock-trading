from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from utils.security import get_db
import models
from utils.security import get_current_user, master_user
from utils.celery_tasks import buy_coin_task, sell_coin_task
from celery_app import celery_app
from schemas import coin_schema, user_schema, trade_schema, transaction_schema, wallet_schema
from utils import operations

router = APIRouter(prefix="/coin", tags=["Coin"])


@router.get("/available_coins", response_model=list[coin_schema.CoinResponse1])
async def show_coins(db: Session = Depends(get_db)) -> object:
    """

    :param db: session for the database
    :return:  show all coins from the coins
    """
    coins = db.query(models.Coin).all()
    return coins


@router.post("/add", response_model=coin_schema.CoinResponse)
async def add_coin(
    coins: coin_schema.CoinCreate,
    db: Session = Depends(get_db),
    # users: models.User = Depends(master_user())
):
    """

    :param coins: create coin schema
    :param db: session for the database
    :return: add coin in the coins table
    """
    return operations.add_coin(db, coins.symbol, coins.name)


@router.post("/buy")
async def buy(
    trade: trade_schema.TradeCreate,
    current_user: models.User = Depends(get_current_user)
) -> dict:
    """

    :param trade: trade create schema
    :param current_user: logged in user
    :return: message and ID for the given task
    """
    task = buy_coin_task.delay(current_user.id, trade.coin_id, trade.quantity, trade.price)
    return {"message": "Buy order submitted", "task_id": task.id}


@router.post("/sell")
async def sell(
    trade: trade_schema.TradeCreate,
    current_user: models.User = Depends(get_current_user)
):
    """

    :param trade: trade create schema
    :param current_user: user which is currently logged in
    :return: status about the request with task_id
    """
    task = sell_coin_task.delay(current_user.id, trade.coin_id, trade.quantity, trade.price)
    return {"message": "Sell order submitted", "task_id": task.id}


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> dict[str, str]:
    """

    :param task_id: id of the task
    :return: result of the request
    """
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}
