from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from app.common.db.core_model import CoreModel
from app.models.balance import Balance


class User(CoreModel):
    __tablename__ = "user"

    chat_id: Mapped[str] = mapped_column(
        String, unique=True, index=True
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    balance: Mapped["Balance"] = relationship("Balance", back_populates="user", uselist=False)