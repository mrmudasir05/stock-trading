# celery_tasks.py
from celery_app import celery_app
from utils import operations
from Database.db import SessionLocal

@celery_app.task
def buy_coin_task(user_id: int, coin_id: int, quantity: float, price: float):
    db = SessionLocal()
    try:
        trade = operations.buy_coin(db, user_id, coin_id, quantity, price)
        return {"status": "success", "trade_id": trade.id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@celery_app.task
def sell_coin_task(user_id: int, coin_id: int, quantity: float, price: float):
    db = SessionLocal()
    try:
        trade = operations.sell_coin(db, user_id, coin_id, quantity, price)
        return {"status": "success", "trade_id": trade.id}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
