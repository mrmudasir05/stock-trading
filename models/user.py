from Database.db import Base
from sqlalchemy import String,TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    balance: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    wallets: Mapped[list["Wallet"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
    trades: Mapped[list["Trade"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )