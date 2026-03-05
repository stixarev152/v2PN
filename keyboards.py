from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ГЛАВНОЕ МЕНЮ
def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("💳 Купить VPN", callback_data="buy")
    )

    kb.add(
        InlineKeyboardButton("👤 Личный кабинет", callback_data="profile")
    )

    kb.add(
        InlineKeyboardButton("👥 Реферальная программа", callback_data="ref")
    )

    kb.add(
        InlineKeyboardButton("📖 Инструкция", callback_data="guide")
    )

    kb.add(
        InlineKeyboardButton("🛠 Техподдержка", callback_data="support")
    )

    return kb


# МЕНЮ ПОКУПКИ
def buy_menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("30 дней — $5", callback_data="buy_30"),
        InlineKeyboardButton("90 дней — $12", callback_data="buy_90"),
        InlineKeyboardButton("365 дней — $40", callback_data="buy_365")
    )

    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )

    return kb


# ЛИЧНЫЙ КАБИНЕТ
def profile_menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("🔑 Мои ключи", callback_data="my_keys")
    )

    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )

    return kb


# РЕФЕРАЛЬНОЕ МЕНЮ
def ref_menu():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("💰 Мой баланс", callback_data="ref_balance")
    )

    kb.add(
        InlineKeyboardButton("🔗 Моя ссылка", callback_data="ref_link")
    )

    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )

    return kb


# КНОПКА НАЗАД
def back_button():
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_main")
    )

    return kb
