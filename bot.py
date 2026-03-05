# bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import BOT_TOKEN
from keyboards import main_menu, vpn_menu
from db import create_tables, add_user
from vpn import create_vpn


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    add_user(message.from_user.id)

    text = """
🚀 Добро пожаловать в VPN сервис!

Что умеет бот:

🌐 Купить VPN
📖 Получить инструкцию
👤 Управлять подпиской

Выберите действие:
"""

    await message.answer(text, reply_markup=main_menu())


@dp.message_handler(lambda message: message.text == "🌐 Купить VPN")
async def buy_vpn(message: types.Message):

    await message.answer(
        "Выберите срок подписки:",
        reply_markup=vpn_menu()
    )


@dp.message_handler(lambda message: message.text == "📖 Инструкция")
async def guide(message: types.Message):

    text = """
📖 Инструкция подключения VPN

1️⃣ Скачайте приложение WireGuard / OpenVPN
2️⃣ Получите конфиг в боте
3️⃣ Импортируйте его в приложение
4️⃣ Подключитесь

Готово ✅
"""

    await message.answer(text)


@dp.message_handler(lambda message: message.text == "👤 Мой аккаунт")
async def account(message: types.Message):

    await message.answer(
        "Ваш аккаунт активен."
    )


@dp.message_handler(lambda message: message.text == "1 месяц")
async def buy1(message: types.Message):

    config = create_vpn(message.from_user.id)

    await message.answer(
        f"Ваш VPN:\n{config}"
    )


if __name__ == "__main__":

    create_tables()

    executor.start_polling(dp)
