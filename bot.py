import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta

TOKEN = "5918595152:AAGNc6Hy00LINGxMo01IJk_hxSw23WgG_zU"
ADMIN_ID = 5186638303

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("vpn.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
referrer INTEGER,
subscription TEXT
)
""")

conn.commit()

# ---------------- KEYBOARDS ----------------

def main_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("👤 Личный кабинет", callback_data="profile"))
    kb.add(InlineKeyboardButton("💳 Купить VPN", callback_data="buy"))
    kb.add(InlineKeyboardButton("👥 Реферальная программа", callback_data="ref"))
    return kb


# ---------------- START ----------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    args = message.get_args()

    cursor.execute("SELECT * FROM users WHERE id=?", (message.from_user.id,))
    user = cursor.fetchone()

    referrer = None

    if args:
        referrer = int(args)

    if not user:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (message.from_user.id, referrer, None)
        )
        conn.commit()

    text = f"""
🚀 Добро пожаловать в VPN сервис

🔒 Безопасный интернет
🌍 Доступ к любым сайтам

Выберите действие ниже 👇
"""

    await message.answer(text, reply_markup=main_menu())


# ---------------- PROFILE ----------------

@dp.callback_query_handler(lambda c: c.data == "profile")
async def profile(callback: types.CallbackQuery):

    cursor.execute("SELECT subscription FROM users WHERE id=?", (callback.from_user.id,))
    sub = cursor.fetchone()[0]

    if sub:
        text = f"""
👤 Ваш кабинет

📅 Подписка до: {sub}
"""
    else:
        text = """
👤 Ваш кабинет

❌ Подписка отсутствует
"""

    await callback.message.edit_text(text, reply_markup=main_menu())


# ---------------- BUY VPN ----------------

@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("1 месяц — $5", callback_data="buy_1"))
    kb.add(InlineKeyboardButton("3 месяца — $12", callback_data="buy_3"))

    await callback.message.edit_text(
        "💳 Выберите тариф",
        reply_markup=kb
    )


# ---------------- PAYMENT STUB ----------------

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def payment(callback: types.CallbackQuery):

    plan = callback.data.split("_")[1]

    if plan == "1":
        price = 5
        days = 30
    else:
        price = 12
        days = 90

    text = f"""
💳 Оплата

Сумма: ${price}

(сюда подключается CryptoBot invoice)
"""

    # тут потом подключается CryptoBot API

    expire = datetime.now() + timedelta(days=days)

    cursor.execute(
        "UPDATE users SET subscription=? WHERE id=?",
        (expire.strftime("%Y-%m-%d"), callback.from_user.id)
    )
    conn.commit()

    await callback.message.edit_text(
        "✅ Подписка активирована"
    )


# ---------------- REF SYSTEM ----------------

@dp.callback_query_handler(lambda c: c.data == "ref")
async def ref(callback: types.CallbackQuery):

    ref_link = f"https://t.me/{(await bot.get_me()).username}?start={callback.from_user.id}"

    cursor.execute("SELECT COUNT(*) FROM users WHERE referrer=?", (callback.from_user.id,))
    refs = cursor.fetchone()[0]

    text = f"""
👥 Реферальная программа

Ваша ссылка:
{ref_link}

Приглашено: {refs}
"""

    await callback.message.edit_text(text, reply_markup=main_menu())


# ---------------- ADMIN PANEL ----------------

@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = """
⚙ Админ панель

/users — список пользователей
/stats — статистика
"""

    await message.answer(text)


# ---------------- USERS LIST ----------------

@dp.message_handler(commands=["users"])
async def users(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    await message.answer(f"👥 Пользователей: {count}")


# ---------------- STATS ----------------

@dp.message_handler(commands=["stats"])
async def stats(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE subscription IS NOT NULL")
    subs = cursor.fetchone()[0]

    text = f"""
📊 Статистика

👥 Пользователей: {users}
💳 Активных подписок: {subs}
"""

    await message.answer(text)


# ---------------- START BOT ----------------

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
