from utils.db import Base
from sqlalchemy import String,TIMESTAMP, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

#Transactions Table
class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))
    amount: Mapped[float] = mapped_column(DECIMAL(20, 8))
    type: Mapped[str] = mapped_column(String(10))  # deposit / withdraw
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")