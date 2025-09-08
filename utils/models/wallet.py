from utils.db import Base
from sqlalchemy import String,TIMESTAMP, ForeignKey,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Wallet Table
class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    balance: Mapped[float] = mapped_column(default=0.0)
    coins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


    # Relationships
    user: Mapped["User"] = relationship(back_populates="wallets")
    coin: Mapped["Coin"] = relationship(back_populates="wallets")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="wallet")
