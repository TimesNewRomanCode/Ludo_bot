from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
import aiofiles
import os

roul_router = Router()

RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]


@roul_router.message(F.text == "/roulette")
async def start_roulette(message: types.Message):
    """Запуск рулетки"""
    builder = InlineKeyboardBuilder()

    # Кнопки 0-36
    builder.button(text="🟢 0", callback_data="roulette_0")
    for i in range(1, 37):
        color = "🔴" if i in RED_NUMBERS else "⚫"
        builder.button(text=f"{color} {i}", callback_data=f"roulette_{i}")

    builder.adjust(3)
    await message.answer(
        "🎰 Выберите число для рулетки:",
        reply_markup=builder.as_markup()
    )


@roul_router.callback_query(F.data.startswith("roulette_"))
async def show_roulette_html(callback: types.CallbackQuery):
    """Показываем HTML рулетку с выбором пользователя"""
    user_choice = int(callback.data.split("_")[1])

    # Читаем HTML файл
    async with aiofiles.open("/home/roman/PycharmProjects/Ludo_bot/app/static/roulette.html", "r") as f:
        html_content = await f.read()

    # Вставляем выбор пользователя в JS
    html_content = html_content.replace(
        "// Установка выбора пользователя (от Python)",
        f"setUserChoice({user_choice});"
    )

    # Отправляем HTML страницу
    await callback.message.answer(
        f"🎰 Ваше число: {user_choice}\n"
        f"Крутите рулетку ниже!",
        reply_markup=InlineKeyboardBuilder().button(
            text="🎰 ИГРАТЬ В РУЛЕТКУ",
            url=f"file:///full/path/to/your/static/roulette.html"
        ).adjust(1).as_markup(),
        parse_mode="HTML"
    )

    await callback.answer()
