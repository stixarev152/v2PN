import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Главное меню
menu = ReplyKeyboardMarkup(resize_keyboard=True)

btn_config = KeyboardButton("📡 Получить VPN конфиг")
btn_buy = KeyboardButton("💳 Купить доступ")
btn_guide = KeyboardButton("📱 Инструкция")
btn_support = KeyboardButton("🛠 Поддержка")

menu.add(btn_config)
menu.add(btn_buy)
menu.add(btn_guide)
menu.add(btn_support)


# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    text = f"""
🚀 Добро пожаловать в VPN сервис

🌐 Быстрый и безопасный VPN
🔐 Полная конфиденциальность
⚡ Высокая скорость соединения

Что вы можете сделать:

📡 Получить VPN конфиг  
💳 Купить доступ  
📱 Посмотреть инструкцию  

Выберите действие ниже 👇
"""

    await message.answer(text, reply_markup=menu)


# ПОЛУЧИТЬ КОНФИГ
@dp.message_handler(lambda message: message.text == "📡 Получить VPN конфиг")
async def get_config(message: types.Message):

    try:
        with open("config.txt", "rb") as file:
            await message.answer_document(
                file,
                caption="📡 Ваш VPN конфиг\n\nИмпортируйте его в приложение."
            )
    except:
        await message.answer("❌ Конфиг временно недоступен.")


# ПОКУПКА
@dp.message_handler(lambda message: message.text == "💳 Купить доступ")
async def buy(message: types.Message):

    text = f"""
💳 Покупка VPN доступа

📅 Тарифы:

1 месяц — 5$
3 месяца — 12$
6 месяцев — 20$

🔥 Что входит:

✔ Безлимитный трафик  
✔ Высокая скорость  
✔ Работает во всех странах  
✔ Поддержка 24/7  

Для покупки напишите администратору:

👤 Админ: @{ADMIN_ID}
"""

    await message.answer(text)


# ИНСТРУКЦИЯ
@dp.message_handler(lambda message: message.text == "📱 Инструкция")
async def guide(message: types.Message):

    text = """
📱 Инструкция по подключению VPN

1️⃣ Скачайте приложение V2Ray

Android:
https://play.google.com/store/apps/details?id=com.v2ray.ang

iPhone:
https://apps.apple.com

Windows:
https://github.com

---

2️⃣ Импортируйте конфиг

📡 Откройте приложение  
📡 Нажмите "Импорт конфигурации"  
📡 Вставьте или загрузите файл

---

3️⃣ Подключитесь

Нажмите кнопку CONNECT

После этого VPN будет работать.

Если возникнут проблемы — напишите в поддержку.
"""

    await message.answer(text)


# ПОДДЕРЖКА
@dp.message_handler(lambda message: message.text == "🛠 Поддержка")
async def support(message: types.Message):

    text = """
🛠 Техническая поддержка

Если возникли проблемы:

• не работает VPN  
• не подключается конфиг  
• проблемы с оплатой  

Напишите администратору:

👤 @yourusername

Мы ответим максимально быстро.
"""

    await message.answer(text)


# АДМИН
@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = """
⚙ Админ панель

Команды:

/users — список пользователей
/broadcast — рассылка
"""

    await message.answer(text)


# СПИСОК ПОЛЬЗОВАТЕЛЕЙ (пока заглушка)
@dp.message_handler(commands=['users'])
# очистка webhook при запуске
async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
