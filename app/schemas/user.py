from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    chat_id: str
    username: str | None
    is_active: bool | None


class UserUpdate(BaseModel):
    username: str | None
    is_active: bool | None
