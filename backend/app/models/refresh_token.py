
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from zoneinfo import ZoneInfo
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"),
                                         nullable=False)
    token : Mapped[str] = mapped_column(Text, unique=True, index=True,  nullable=False)
    device_info: Mapped[str] = mapped_column(Text, nullable=True)
    is_revoked : Mapped[bool] = mapped_column(Boolean, default=False)
    expire_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)       
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Vienna"))
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(ZoneInfo("Europe/Vienna")),
        onupdate=lambda: datetime.now(ZoneInfo("Europe/Vienna"))
    )
    user: Mapped["User"] = relationship(argument="User", backref="refresh_tokens")


    