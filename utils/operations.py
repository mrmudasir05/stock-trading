from sqlalchemy.orm import Session
import models
from utils.security import hash_password
from fastapi import HTTPException
from schemas import user_schema


def create_user(db: Session, user_: user_schema.UserCreate):
    # check if username or email already exists
    existing_user = db.query(models.User).filter(
        (models.User.username == user_.username) | (models.User.email == user_.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )
    hashed_pw = hash_password(user_.password)
    db_user = models.User(
        username=user_.username,
        email=user_.email,
        password_hash=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: user_schema.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None  # User not found
    db.delete(db_user)
    db.commit()
    return db_user


def deposit_wallet(db: Session, user_id: int, coin_id: int, amount: float):
    wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    if not wallet:
        raise HTTPException(status_code=400, detail="Wallet not exists")

    if user.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient Balance to deposit money to wallet")
    user.balance -=amount
    wallet.balance += amount
    # Record transaction
    tx = models.Transaction(wallet=wallet, amount=amount, type="deposit")
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet


def wallet_create(db: Session, user_id: int, coin_id: int):
    wallet = models.Wallet(user_id=user_id, coin_id=coin_id, balance=0.0, coins = 0)
    coin = db.query(models.Coin).filter_by(id=coin_id).first()
    if not coin:
        raise HTTPException(status_code=400, detail="Coin not exists")

    existing_wallet = db.query(models.Wallet).filter(models.Wallet.coin_id == wallet.coin_id).first()
    if existing_wallet:
        raise HTTPException(status_code=400, detail="Wallet already created")

    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet


def withdraw_wallet(db: Session, user_id: int, coin_id: int, amount: float):
    wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    user = db.query(models.User).filter_by(id=user_id).first()
    if not wallet or wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    wallet.balance -= amount
    user.balance +=amount
    # Record transaction
    tx = models.Transaction(wallet=wallet, amount=amount, type="withdraw")
    db.add(tx)
    db.commit()
    db.refresh(wallet)
    return wallet

# 🔹 Buy Coin
def buy_coin(db: Session, user_id: int, coin_id: int, quantity: float, price: float):
    coin = db.query(models.Coin).filter_by(id=coin_id).first()
    wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    if not coin :
        raise HTTPException(status_code=400, detail="Invalid coin_id")
    coin_wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    proceeds = quantity * price
    if not coin_wallet:
        raise HTTPException(status_code=400, detail="Wallet dont exists")
    if not coin_wallet or coin_wallet.balance < proceeds:
        raise HTTPException(status_code=400, detail="Insufficient Balance to buy")
    coin_wallet.balance -= proceeds
    wallet.coins+=quantity
    db.add(models.Transaction(wallet=coin_wallet, amount=proceeds, type="withdraw"))
    trade = models.Trade(user_id=user_id, coin_id=coin_id, trade_type="buy", quantity=quantity, price=price)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

# 🔹 Sell Coin
def sell_coin(db: Session, user_id: int, coin_id: int, quantity: float, price: float):
    coin = db.query(models.Coin).filter_by(id=coin_id).first()
    wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    if not coin :
        raise HTTPException(status_code=400, detail="Invalid coin_id")
    coin_wallet = db.query(models.Wallet).filter_by(user_id=user_id, coin_id=coin_id).first()
    proceeds = quantity * price
    if not coin_wallet or wallet.coins < quantity:
        raise HTTPException(status_code=400, detail="Insufficient coins to sell")
    coin_wallet.balance += proceeds
    wallet.coins -= quantity
    db.add(models.Transaction(wallet=coin_wallet, amount=proceeds, type="deposit"))
    trade = models.Trade(user_id=user_id, coin_id=coin_id, trade_type="sell", quantity=quantity, price=price)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

def add_balance(db: Session, user_id: int, amount: float):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    user.balance += amount
    db.commit()
    db.refresh(user)
    return user

def add_coin(db:Session, symbol:str, name:str):
    coin = models.Coin(symbol = symbol, name = name)
    db.add(coin)
    db.commit()
    db.refresh(coin)
    return coin