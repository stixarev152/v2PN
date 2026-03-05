import time
from aiogram import Bot,Dispatcher,types
from aiogram.utils import executor

import db
import keyboards
import cryptobot
import vpn
import config


bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message:types.Message):

    args = message.get_args()

    ref = None
    if args:
        ref = int(args)

    db.add_user(message.from_user.id,ref)

    await message.answer(
        "🚀 Добро пожаловать в VPN сервис",
        reply_markup=keyboards.main_menu()
    )


@dp.callback_query_handler(lambda c:c.data=="buy")
async def buy(call:types.CallbackQuery):

    await call.message.edit_text(
        "Выберите тариф",
        reply_markup=keyboards.buy_menu()
    )


@dp.callback_query_handler(lambda c:c.data.startswith("buy_"))
async def buy_tariff(call:types.CallbackQuery):

    days = int(call.data.split("_")[1])

    price = {
        30:config.PRICE_30,
        90:config.PRICE_90,
        365:config.PRICE_365
    }[days]

    url,invoice = crypto.create_invoice(price)

    await call.message.answer(
        f"Оплатите VPN\n\n{url}"
    )

    while True:

        status = crypto.check_invoice(invoice)

        if status == "paid":

            key = vpn.create_vpn_key()

            db.add_sub(call.from_user.id,key,days)

            await call.message.answer(
                f"✅ Оплата прошла\n\nВаш VPN ключ:\n{key}"
            )

            break

        await asyncio.sleep(10)


@dp.callback_query_handler(lambda c:c.data=="profile")
async def profile(call:types.CallbackQuery):

    sub = db.get_sub(call.from_user.id)

    if not sub:
        await call.message.answer("❌ Нет активной подписки")
        return

    key,expire = sub

    days = int((expire-time.time())/86400)

    await call.message.answer(
        f"""
👤 Личный кабинет

🔑 Ключ:
{key}

⏳ Осталось:
{days} дней
"""
    )


@dp.callback_query_handler(lambda c:c.data=="ref")
async def ref(call:types.CallbackQuery):

    link = f"https://t.me/{(await bot.get_me()).username}?start={call.from_user.id}"

    await call.message.answer(
        f"""
👥 Реферальная программа

Ваша ссылка:

{link}
"""
    )


@dp.callback_query_handler(lambda c:c.data=="back")
async def back(call:types.CallbackQuery):

    await call.message.edit_text(
        "Главное меню",
        reply_markup=keyboards.main_menu()
    )


executor.start_polling(dp)
