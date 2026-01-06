from aiogram import BaseMiddleware


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_generator):
        self.session_generator = session_generator

    async def __call__(self, handler, event, data):
        agen = self.session_generator()
        session = await anext(agen)
        try:
            data["session"] = session
            return await handler(event, data)
        finally:
            await session.close()
            await agen.aclose()
