import asyncio
import logging

import aiofiles
from aiohttp import web

from app.keyboards.commands import set_commands
from app.core.create_bot import bot, dp
from app.router.common import (
    start_router,
    balance_router, roul_router,
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
        roul_router
    )

    await set_commands(bot)

    # Функция для отдачи HTML рулетки
    async def handle_roulette(request):
        async with aiofiles.open("static/roulette.html", "r") as f:
            html = await f.read()
        return web.Response(text=html, content_type="text/html")

    # Запускаем веб-сервер
    app = web.Application()
    app.router.add_get('/roulette.html', handle_roulette)

    # Запускаем веб-сервер в фоне
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)

    print("Веб-сервер запущен на порту 8080")
    await site.start()

    # Запускаем бота
    print("Бот запущен")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())