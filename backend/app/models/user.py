

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


import bcrypt
from click import DateTime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
class User(Base):

    __tablename__ = "users"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(
    DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Vienna"))
    )

    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Vienna")),
        onupdate=lambda: datetime.now(ZoneInfo("Europe/Vienna"))
    )

    def set_password(self, password: str) -> None:
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), salt).decode("utf-8")
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password.encode("utf-8"))