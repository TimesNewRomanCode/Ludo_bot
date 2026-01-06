from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repository
from app.schemas.user import UserCreate


async def register_user(
    session: AsyncSession,
    chat_id: int,
    username: str
):
    chat_id = str(chat_id)

    user = await user_repository.get_by_chat_id(session, chat_id)
    if user:
        user.username = username
        user.is_active = True
        await session.commit()
    else:
        user = await user_repository.create(
            session,
            obj_in=UserCreate(
                username=username, chat_id=chat_id, is_active=True
            ),
        )

    return user
