from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_gallery_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Баланс"), KeyboardButton(text="Играть")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard