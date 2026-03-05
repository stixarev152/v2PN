import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=5918595152:AAGNc6Hy00LINGxMo01IJk_hxSw23WgG_zU)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("📡 Получить конфиг"))
menu.add(KeyboardButton("💳 Купить доступ"))
menu.add(KeyboardButton("ℹ️ Инструкция"))

def load_config():
    with open("config.txt", "r", encoding="utf-8") as f:
        return f.read()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    text = """
🚀 Добро пожаловать

Это VPN сервис.

Выберите действие ниже.
"""
    await message.answer(text, reply_markup=menu)

@dp.message_handler(lambda message: message.text == "📡 Получить конфиг")
async def get_config(message: types.Message):

    config = load_config()

    await message.answer(
        f"Ваш конфиг:\n\n{config}"
    )

@dp.message_handler(lambda message: message.text == "💳 Купить доступ")
async def buy(message: types.Message):

    text = """
💳 Покупка доступа

Цена: 5$

Напишите администратору:
@yourusername
"""

    await message.answer(text)

@dp.message_handler(lambda message: message.text == "ℹ️ Инструкция")
async def guide(message: types.Message):

    text = """
📱 Как подключиться

1 Скачать V2Ray
2 Импортировать конфиг
3 Подключиться

Если есть проблемы — пишите админу.
"""

    await message.answer(text)

@dp.message_handler(commands=['users'])
async def users(message: types.Message):

    if message.from_user.id == ADMIN_ID:
        await message.answer("Админ панель пока пустая")

if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
