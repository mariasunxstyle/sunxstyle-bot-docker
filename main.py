import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from steps import steps

print("🟢 Бот стартует...")

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["creator", "administrator", "member"]
    except:
        return False

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    if not await check_subscription(message.from_user.id):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Я подписался", url="https://t.me/sunxstyle"))
        await message.answer("Подпишись на канал @sunxstyle, чтобы начать ☀️", reply_markup=kb)
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for step in steps:
        m = step['duration_min']
        keyboard.add(f"Шаг {step['step']} ({m} мин)")
    keyboard.add("ℹ️ Инфо")
    await message.answer("Привет, солнце! ☀️ Выбери шаг:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text.startswith("Шаг"))
async def handle_step(message: types.Message):
    await message.reply("Следи за временем и положением тела ☀️")

@dp.message_handler(lambda message: message.text == "ℹ️ Инфо")
async def handle_info(message: types.Message):
    await message.reply("ℹ️ Метод суперкомпенсации — это безопасный пошаговый загар...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
