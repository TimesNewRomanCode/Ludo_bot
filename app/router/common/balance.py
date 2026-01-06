from aiogram import Router, types, F
from aiogram.filters import Command, or_f
from aiogram.types import LabeledPrice
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.payment_key_inline import get_balance_keyboard, get_option_stars_keyboard, get_payment_keyboard
from app.services.balance import balance_user, buy_balance

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

@balance_router.callback_query(F.data.startswith("buy_stars"))
async def buy_stars(callback: types.CallbackQuery):
    kb = get_option_stars_keyboard()
    await callback.message.edit_text(
        "Выберите количество звезд для покупки:",
        reply_markup=kb.as_markup()
    )
    await callback.answer()


@balance_router.callback_query(F.data.startswith("buy_"))
async def process_star_selection(callback: types.CallbackQuery):
    stars_count = int(callback.data.split("_")[1])

    kb = get_payment_keyboard(stars_count)

    await callback.message.edit_text(
        f"⭐ Подтвердите покупку {stars_count} звезд\n"
        f"(средства будут списаны с вашего баланса Telegram Stars)",
        reply_markup=kb
    )
    await callback.answer()


@balance_router.callback_query(F.data.startswith("pay_"))
async def create_star_invoice(callback: types.CallbackQuery):
    stars_count = int(callback.data.split("_")[1])  # pay_5 → 5

    prices = [LabeledPrice(label=f"⭐ {stars_count} Звезд", amount=stars_count)]

    await callback.message.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="⭐ Покупка звезд для Ludo Bot",
        description=f"{stars_count} звезд = {stars_count * 50} Ludocoins",
        payload=f"ludo_stars_{stars_count}_{callback.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices
    )
    await callback.answer("📤 Счет отправлен на оплату!")


@balance_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@balance_router.message(F.successful_payment)
async def process_stars_payment(message: types.Message, session: AsyncSession):
    chat_id = str(message.chat.id)
    stars_count = int(message.successful_payment.total_amount)
    await buy_balance(session, chat_id, stars_count)
    await message.answer(
        f"🎉 Оплата прошла успешно!\n"
        f"⭐ Вы купили {stars_count} звезд\n"
        f"💰 Начислено {stars_count * 50} Ludocoins!\n\n"
        f"/getbalance - проверить баланс"
    )


@balance_router.callback_query(F.data == "back_balance")
async def back_to_balance(callback: types.CallbackQuery, session: AsyncSession):
    chat_id = callback.from_user.id
    money = await balance_user(session, chat_id)
    kb = get_balance_keyboard()
    await callback.message.edit_text(
        f"Дорогой игрок, у вас: {money} Ludocoin",
        reply_markup=kb.as_markup()
    )

