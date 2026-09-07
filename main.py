# VENV Virtual Environment
#
# Пользователь -> Telegram -> Bot API -> Наш Python Code -> Bot API -> Telegram -> Пользователь

# import asyncio
#
# async def main():
#     print("Сервер просыпается...")
#     await asyncio.sleep(1)
#
#     print("Сервер проснулся")
#
# asyncio.run(main())

import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()


# здесь сделали кнопки для бота
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Статус"),
            KeyboardButton(text="😂 Шутка")
        ],
        [
            KeyboardButton(text="🆘 Помощь")
        ],
    ],
    resize_keyboard=True,
)


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Здравствуй, {message.from_user.first_name}!👋🏼\n"
        "Я дежурный бот Серверной комнаты.\n"
        "Все системы (кроме моей мотивации) в норме.",
        reply_markup=main_keyboard  # показываем кнопки пользователю
    )


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — знакомство\n"
        "/status — статус серверов\n"
        "/joke — техническая шутка дня\n"
    )


# сделали команду для проверки серверов
@router.message(Command("status"))
async def status(message: Message):
    await message.answer(
        "💻 web_server — жив\n"
        "🖨️ db_server — жив, но грустит\n"
        "💾 backup_server — не отвечает уже 3 дня (это нормально)"
    )


# сделали команду для шутки
@router.message(Command("joke"))
async def joke(message: Message):
    await message.answer(
        "Почему программисты путают Хэллоуин и Рождество?\n"
        "Потому что OCT 31 == DEC 25."
    )


# привязали кнопку к статусу
@router.message(lambda m: m.text == "📊 Статус")
async def button_status(message: Message):
    await status(message)


# привязали кнопку к шутке
@router.message(lambda m: m.text == "😂 Шутка")
async def button_joke(message: Message):
    await joke(message)


# привязали кнопку к помощи
@router.message(lambda m: m.text == "🆘 Помощь")
async def button_help(message: Message):
    await help(message)


# сюда попадает всё, что бот не понял
@router.message()
async def echo_all(message: Message):
    await message.answer(
        f"Не понял сообщение '{message.text}',\n"
        "Наберите /help — я не телепат, я бот."
    )


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


# В итоге сделали команды, кнопки и обработку непонятных сообщений.
# Теперь бот стал удобнее и умеет больше.