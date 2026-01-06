from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import User


class Balance(CoreModel):
    __tablename__ = "Balance"

    money: Mapped[float] = mapped_column(Float, index=True, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.chat_id"), unique=True)
    user: Mapped["User"] = relationship("User", back_populates="balance")