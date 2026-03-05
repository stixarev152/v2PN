# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("🌐 Купить VPN"),
        KeyboardButton("👤 Мой аккаунт")
    )

    kb.add(
        KeyboardButton("📖 Инструкция"),
        KeyboardButton("🆘 Поддержка")
    )

    return kb


def vpn_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    kb.add(
        KeyboardButton("1 месяц"),
        KeyboardButton("3 месяца")
    )

    kb.add(
        KeyboardButton("6 месяцев"),
        KeyboardButton("12 месяцев")
    )

    kb.add(
        KeyboardButton("⬅ Назад")
    )

    return kb
