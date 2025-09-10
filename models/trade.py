from Database.db import Base
from sqlalchemy import String,TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    coin_id: Mapped[int] = mapped_column(ForeignKey("coins.id"))
    trade_type: Mapped[str] = mapped_column(String(10))  # buy / sell
    quantity: Mapped[float] = mapped_column(DECIMAL(20, 8))
    price: Mapped[float] = mapped_column(DECIMAL(20, 2))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="trades")
    coin: Mapped["Coin"] = relationship(back_populates="trades")
