from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, or_f
from aiogram.types import WebAppInfo

roul_router = Router()

RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Ваш IP или домен
WEBAPP_URL = "http://localhost:8080/roulette.html"


@roul_router.message(or_f(Command("roulette"), F.text == "🎰 Рулетка"))
async def start_roulette(message: types.Message):
    builder = InlineKeyboardBuilder()

    # Добавляем числа
    builder.button(text="🟢 0", callback_data="bet_0")
    for i in range(1, 37):
        color = "🔴" if i in RED_NUMBERS else "⚫"
        builder.button(text=f"{color} {i}", callback_data=f"bet_{i}")

    builder.adjust(3)

    await message.answer(
        "🎰 *Выберите число для ставки:*\n"
        "Коэффициент: 35:1",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )


@roul_router.callback_query(F.data.startswith("bet_"))
async def place_bet(callback: types.CallbackQuery):
    user_choice = callback.data[4:]  # bet_23 -> 23

    # Создаем кнопку Web App
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎰 Крутить рулетку!",
        web_app=WebAppInfo(url=f"{WEBAPP_URL}?bet={user_choice}")
    )

    await callback.message.answer(
        f"✅ *Ставка принята!*\n"
        f"🎯 Ваше число: {user_choice}\n"
        f"💰 Ставка: 100 монет\n\n"
        f"Нажмите кнопку ниже чтобы крутить:",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )
    await callback.answer()


@roul_router.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    """Обрабатываем результат из Web App"""
    import json

    data = json.loads(message.web_app_data.data)

    if data.get("type") == "roulette_result":
        winning_number = data.get("winning_number")
        user_bet = data.get("user_bet")
        is_win = data.get("is_win", False)

        # Определяем цвет числа
        if winning_number == 0:
            color = "🟢"
        elif winning_number in RED_NUMBERS:
            color = "🔴"
        else:
            color = "⚫"

        if is_win:
            result = "🎉 *ВЫ ВЫИГРАЛИ!* 🎉"
            win_amount = 3500  # 100 * 35
        else:
            result = "😔 *Проигрыш*"
            win_amount = -100

        await message.answer(
            f"🎰 *РЕЗУЛЬТАТ РУЛЕТКИ*\n\n"
            f"{color} *Выпало число:* {winning_number}\n"
            f"🎯 *Ваша ставка:* {user_bet}\n\n"
            f"{result}\n"
            f"💰 *Сумма:* {win_amount} монет\n\n"
            f"🎰 /roulette - играть снова",
            parse_mode="Markdown"
        )