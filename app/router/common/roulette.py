from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import random

roul_router = Router()

RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
ROULETTE_URL = "https://htmlpreview.github.io/?https://raw.githubusercontent.com/TimesNewRomanCode/Ludo_bot/roulette-test/app/static/roulette.html"


@roul_router.message(F.text == "/roulette")
async def start_roulette(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="🟢 0", callback_data="roulette_0")
    for i in range(1, 37):
        color = "🔴" if i in RED_NUMBERS else "⚫"
        builder.button(text=f"{color} {i}", callback_data=f"roulette_{i}")
    builder.adjust(3)
    await message.answer("🎰 Выберите число:", reply_markup=builder.as_markup())


@roul_router.callback_query(F.data.startswith("roulette_"))
async def show_roulette_html(callback: types.CallbackQuery):
    user_choice = int(callback.data.split("_")[1])

    kb = InlineKeyboardBuilder()
    kb.button(text="🎰 ИГРАТЬ В РУЛЕТКУ", url=f"{ROULETTE_URL}?choice={user_choice}")
    kb.adjust(1)

    await callback.message.answer(
        f"🎰 **Ваш выбор: {user_choice}**\n"
        f"🔥 Кликните → крутите → бот получит результат!",
        reply_markup=kb.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()


@roul_router.message(F.text.startswith("roulette_result_"))
async def roulette_result(message: types.Message):
    parts = message.text.split("_")
    result = int(parts[2])
    user_choice = int(parts[3]) if len(parts) > 3 else None

    win_status = "🎉 **ВЫИГРЫШ x35!**" if user_choice and result == user_choice else "😔 Проигрыш"

    await message.answer(
        f"🎰 **РЕЗУЛЬТАТ: {result}**\n"
        f"🎯 {'Выбор: ' + str(user_choice) if user_choice else ''}\n\n"
        f"{win_status}\n\n/roulette — еще раз!",
        parse_mode="Markdown"
    )
