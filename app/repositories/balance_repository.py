from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.db.base_repository import BaseRepository
from app.models import Balance
from app.schemas.balance import BalanceCreate, BalanceUpdate


class BalanceRepository(BaseRepository[Balance, BalanceCreate, BalanceUpdate]):
    @staticmethod
    async def get_balance_by_id(session: AsyncSession, chat_id: str):
        stmt = select(Balance).where(Balance.user_id == chat_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_balance_by_chat_id(session: AsyncSession, chat_id: int):
        stmt = (
            select(Balance).where(Balance.user_id == chat_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

balance_repository = BalanceRepository(Balance)