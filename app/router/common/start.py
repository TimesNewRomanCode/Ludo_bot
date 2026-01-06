from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.manager_keyboards import get_gallery_keyboard
from app.services.balance import register_balance
from app.services.user import register_user

start_router = Router()

@start_router.message(CommandStart())
async def message_handler(message: types.Message, session: AsyncSession):
    kb = get_gallery_keyboard()
    await register_user(session, message.chat.id, message.from_user.username)
    await register_balance(session, message.chat.id)
    print(f"Новый пользователь{message.from_user.username}")
    await message.answer("Добро пожаловать в игру, где вы либо приумножите свое состояние, либо потеряте всёёё!!!", reply_markup=kb)