from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.payment_key_inline import get_balance_keyboard
from app.services.balance import balance_user

balance_router = Router()


@balance_router.message(or_f(Command("getbalance"), F.text == "Баланс"))
async def message_balance(message: types.Message,  session: AsyncSession):
    chat_id = message.chat.id
    money = await balance_user(session, chat_id)
    kb = get_balance_keyboard()
    await message.answer(
        f"Дорогой игрок, у вас: {money} Ludocoin",
        reply_markup=kb.as_markup()
    )