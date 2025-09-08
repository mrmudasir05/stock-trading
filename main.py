from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.security import verify_password, create_access_token, get_db
from utils import schemas, operations
from utils import models
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import get_current_user, master_user
from utils.celery_tasks import buy_coin_task, sell_coin_task
from celery_app import celery_app

app = FastAPI()

@app.get("/users", response_model=list[schemas.UserInfo])
def get_users(db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    users = db.query(models.User).all()
    return users

@app.get("/user/info", response_model=schemas.UserMe)
def get_user(current_user: models.User = Depends(get_current_user)):
    return current_user

@app.get("/user/wallets", response_model=schemas.UserWallets)
def get_user(current_user: models.User = Depends(get_current_user)):
    return {"wallets": current_user.wallets}

@app.get("/user/trades", response_model=schemas.UserTrade)
def get_user(current_user: models.User = Depends(get_current_user)):
    return {"trades" : current_user.trades}


@app.get("/available_coins", response_model=list[schemas.CoinResponse1])
def show_coins(db: Session = Depends(get_db)):
    coins = db.query(models.Coin).all()
    return coins

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return operations.create_user(db, user)

@app.put("/users/update", response_model=schemas.UserInfo)
def update_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_user = operations.update_user(db, current_user.id, user_update)
    return db_user

@app.delete("/users/me")
def delete_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_user = operations.delete_user(db, current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/coins/add", response_model=schemas.CoinResponse)
def add_coin(
    coin: schemas.CoinCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(master_user)
):
    return operations.add_coin(db, coin.symbol, coin.name)

@app.post("/user/recharge", response_model=schemas.RechargeResponse)
def recharge_balance(
    recharge: schemas.BalanceRecharge,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if recharge.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    user = operations.add_balance(db, current_user.id, recharge.amount)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/wallets/deposit", response_model=schemas.WalletResponse)
def deposit(
    request: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return operations.deposit_funds(db, current_user.id, request.wallet_id, request.amount)

@app.post("/wallets/withdraw", response_model=schemas.WalletResponse)
def withdraw(
    request: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return operations.withdraw_funds(db, current_user.id, request.wallet_id, request.amount)

# @app.post("/coins/buy", response_model=schemas.TradeResponse)
# def buy(
#     trade: schemas.TradeCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     return operations.buy_coin(db, current_user.id, trade.coin_id, trade.quantity, trade.price)
#
# @app.post("/coins/sell", response_model=schemas.TradeResponse)
# def sell(
#     trade: schemas.TradeCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     return operations.sell_coin(db, current_user.id, trade.coin_id, trade.quantity, trade.price)

@app.post("/coins/buy")
def buy(
    trade: schemas.TradeCreate,
    current_user: models.User = Depends(get_current_user)
):
    task = buy_coin_task.delay(current_user.id, trade.coin_id, trade.quantity, trade.price)
    return {"message": "Buy order submitted", "task_id": task.id}

@app.post("/coins/sell")
def sell(
    trade: schemas.TradeCreate,
    current_user: models.User = Depends(get_current_user)
):
    task = sell_coin_task.delay(current_user.id, trade.coin_id, trade.quantity, trade.price)
    return {"message": "Sell order submitted", "task_id": task.id}


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}