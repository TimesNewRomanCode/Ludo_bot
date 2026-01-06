from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Balance
from app.repositories import balance_repository
from app.repositories.balance_repository import BalanceRepository
from app.schemas.balance import BalanceCreate


async def balance_user(
    session: AsyncSession,
    chat_id: int,
):
    chat_id = str(chat_id)
    balance = await BalanceRepository.get_balance_by_id(session, chat_id)

    return balance.money

async def register_balance(
    session: AsyncSession,
    chat_id: int,
):
    user_id = str(chat_id)

    user = await balance_repository.get_balance_by_chat_id(session, user_id)
    if user:
        user.is_active = True
        await session.commit()
    else:
        user = await balance_repository.create(
            session,
            obj_in=BalanceCreate(
             user_id=user_id, is_active=True
            ),
        )

    return user

async def buy_balance(
    session: AsyncSession,
    chat_id: str,
    stars_count: int
):
    user_id = str(chat_id)
    balance = await BalanceRepository.get_balance_by_id(session, user_id)
    if balance:
        balance.money += stars_count * 50
    else:
        balance = Balance(user_id=user_id, money=stars_count * 50)
        session.add(balance)

    await session.commit()