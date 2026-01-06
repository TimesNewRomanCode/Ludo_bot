from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_balance_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="Пополнить баланс", callback_data="buy_stars")
    builder.button(text="Дайте пж 100 коинов, умоляю", callback_data="play")
    builder.adjust(1)
    return builder

def get_option_stars_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="⭐ 1 Звезда", callback_data="buy_1_star")
    builder.button(text="⭐ 5 Звезд", callback_data="buy_5_stars")
    builder.button(text="⭐ 10 Звезд", callback_data="buy_10_stars")
    builder.button(text="⭐ 25 Звезд", callback_data="buy_25_stars")
    builder.button(text="К балансу", callback_data="back_balance")
    builder.adjust(1)
    return builder

def get_payment_keyboard(stars_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить", callback_data=f"pay_{stars_count}")
    builder.button(text="Отмена", callback_data="back_balance")
    builder.adjust(2)
    return builder.as_markup()

def get_back_balance_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 К балансу", callback_data="back_balance")
    return builder