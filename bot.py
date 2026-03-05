import logging
import sqlite3
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("👤 Личный кабинет", callback_data="profile"),
        InlineKeyboardButton("💳 Купить VPN", callback_data="buy"),
        InlineKeyboardButton("👥 Реферальная программа", callback_data="ref"),
        InlineKeyboardButton("📱 Инструкция", callback_data="guide"),
        InlineKeyboardButton("🛠 Поддержка", callback_data="support")
    )

    return kb


def back_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("⬅ Назад", callback_data="back"))
    return kb


# ---------------- START ----------------

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    args = message.get_args()

    cursor.execute("SELECT * FROM users WHERE id=?", (message.from_user.id,))
    user = cursor.fetchone()

    referrer = None

    if args:
        try:
            referrer = int(args)
        except:
            referrer = None

    if not user:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (message.from_user.id, referrer, None)
        )
        conn.commit()

    text = """
🚀 Добро пожаловать в VPN сервис

🔒 Безопасный интернет  
🌍 Доступ к любым сайтам  
⚡ Высокая скорость

Выберите действие 👇
"""

    await message.answer(text, reply_markup=main_menu())


# ---------------- BACK ----------------

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):

    await callback.message.edit_text(
        "🏠 Главное меню",
        reply_markup=main_menu()
    )


# ---------------- PROFILE ----------------

@dp.callback_query_handler(lambda c: c.data == "profile")
async def profile(callback: types.CallbackQuery):

    cursor.execute(
        "SELECT subscription FROM users WHERE id=?",
        (callback.from_user.id,)
    )

    sub = cursor.fetchone()[0]

    if sub:
        text = f"""
👤 Личный кабинет

📅 Подписка активна до:
{sub}
"""
    else:
        text = """
👤 Личный кабинет

❌ У вас нет активной подписки
"""

    await callback.message.edit_text(text, reply_markup=back_menu())


# ---------------- BUY ----------------

@dp.callback_query_handler(lambda c: c.data == "buy")
async def buy(callback: types.CallbackQuery):

    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton("1 месяц — $5", callback_data="buy_1"),
        InlineKeyboardButton("3 месяца — $12", callback_data="buy_3"),
        InlineKeyboardButton("⬅ Назад", callback_data="back")
    )

    await callback.message.edit_text(
        "💳 Выберите тариф",
        reply_markup=kb
    )


# ---------------- PAYMENT STUB ----------------

@dp.callback_query_handler(lambda c: c.data.startswith("buy_"))
async def payment(callback: types.CallbackQuery):

    plan = callback.data.split("_")[1]

    if plan == "1":
        days = 30
    else:
        days = 90

    expire = datetime.now() + timedelta(days=days)

    cursor.execute(
        "UPDATE users SET subscription=? WHERE id=?",
        (expire.strftime("%Y-%m-%d"), callback.from_user.id)
    )

    conn.commit()

    await callback.message.edit_text(
        "✅ Подписка активирована",
        reply_markup=main_menu()
    )


# ---------------- REF SYSTEM ----------------

@dp.callback_query_handler(lambda c: c.data == "ref")
async def ref(callback: types.CallbackQuery):

    bot_info = await bot.get_me()

    ref_link = f"https://t.me/{bot_info.username}?start={callback.from_user.id}"

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE referrer=?",
        (callback.from_user.id,)
    )

    refs = cursor.fetchone()[0]

    text = f"""
👥 Реферальная программа

Ваша ссылка:
{ref_link}

Приглашено пользователей:
{refs}
"""

    await callback.message.edit_text(text, reply_markup=back_menu())


# ---------------- GUIDE ----------------

@dp.callback_query_handler(lambda c: c.data == "guide")
async def guide(callback: types.CallbackQuery):

    text = """
📱 Инструкция подключения

1️⃣ Скачайте приложение V2Ray

Android  
https://play.google.com/store/apps/details?id=com.v2ray.ang

iPhone  
https://apps.apple.com

2️⃣ Импортируйте конфиг

3️⃣ Нажмите CONNECT
"""

    await callback.message.edit_text(text, reply_markup=back_menu())


# ---------------- SUPPORT ----------------

@dp.callback_query_handler(lambda c: c.data == "support")
async def support(callback: types.CallbackQuery):

    text = """
🛠 Поддержка

Если возникли проблемы:

• VPN не работает  
• Конфиг не подключается  
• Проблемы с оплатой  

Напишите администратору
"""

    await callback.message.edit_text(text, reply_markup=back_menu())


# ---------------- ADMIN PANEL ----------------

@dp.message_handler(commands=["admin"])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = """
⚙ Админ панель

/users — количество пользователей  
/stats — статистика
"""

    await message.answer(text)


# ---------------- USERS ----------------

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
