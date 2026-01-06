from pydantic import BaseModel


class BalanceCreate(BaseModel):
    user_id: str
    is_active: bool | None


class BalanceUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None
