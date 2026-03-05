from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


def main_menu():
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton("💳 Купить VPN",callback_data="buy"))
    kb.add(InlineKeyboardButton("👤 Личный кабинет",callback_data="profile"))
    kb.add(InlineKeyboardButton("👥 Реферальная программа",callback_data="ref"))

    return kb


def buy_menu():
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("30 дней",callback_data="buy_30"),
        InlineKeyboardButton("90 дней",callback_data="buy_90")
    )

    kb.add(
        InlineKeyboardButton("365 дней",callback_data="buy_365")
    )

    kb.add(InlineKeyboardButton("⬅ Назад",callback_data="back"))

    return kb


def back():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅ Назад",callback_data="back"))
    return kb
