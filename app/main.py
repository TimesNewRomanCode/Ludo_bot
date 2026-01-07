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
    polling_task = asyncio.create_task(dp.start_polling(bot))

    await asyncio.gather(polling_task)

    async def handle_roulette(request):
        async with aiofiles.open("static/roulette.html", "r") as f:
            return web.Response(text=await f.read(), content_type="text/html")
    print("dvmdkmks")
    app = web.Application()
    app.router.add_static('/static/', path='static/', show_index=True)
    app.router.add_get('/roulette.html', handle_roulette)
    web.run_app(app, host='0.0.0.0', port=8080)
    logging.info("Бот завершает работу.")
    await bot.delete_webhook(drop_pending_updates=True)
