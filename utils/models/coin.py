from utils.db import Base
from sqlalchemy import String,TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Coin(Base):
    __tablename__ = "coins"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    wallets: Mapped[list["Wallet"]] = relationship(back_populates="coin")
    trades: Mapped[list["Trade"]] = relationship(back_populates="coin")
