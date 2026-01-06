import asyncio
import logging

from app.keyboards.commands import set_commands
from app.core.create_bot import bot, dp
from app.router.common import (
    start_router,
    balance_router,
)
from app.router.admin import message_chat_all_router, photo_chat_all_router
from app.core.database import get_session
from app.middlewares.db import DbSessionMiddleware


async def main():
    print("Запуск бота...")

    dp.message.middleware(DbSessionMiddleware(get_session))
    dp.callback_query.middleware(DbSessionMiddleware(get_session))

    dp.include_routers(
        start_router,
        message_chat_all_router,
        photo_chat_all_router,
        balance_router,
    )
    await set_commands(bot)
    polling_task = asyncio.create_task(dp.start_polling(bot))

    await asyncio.gather(polling_task)

    logging.info("Бот завершает работу.")
    await bot.delete_webhook(drop_pending_updates=True)
