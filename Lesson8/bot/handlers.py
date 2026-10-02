import os
import httpx

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

router = Router()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🤖 Спросить AI"
                )
            ],
            [
                KeyboardButton(
                    text="ℹ️ Помощь"
                )
            ],
        ],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "👋 Привет!\n\n"
        "Я AI-помощник на Gemini.\n\n"
        "Просто отправьте мне любой вопрос.\n\n"
        "/start — главное меню\n"
        "/help — помощь",
        reply_markup=main_keyboard(),
    )


@router.message(Command("help"))
@router.message(F.text == "ℹ️ Помощь")
async def help_handler(message: Message):

    await message.answer(
        "💡 Просто отправьте мне вопрос.\n\n"
        "Например:\n"
        "• Объясни Django ORM\n"
        "• Что такое 67 Мем?\n"
        "• Исправь ошибку Python"
    )


@router.message(F.text == "🤖 Спросить AI")
async def ask_ai_button(message: Message):

    await message.answer(
        "Напишите свой вопрос 👇"
    )


async def ask_gemini(prompt: str) -> str:

    if not GEMINI_API_KEY:
        return (
            "❌ GEMINI_API_KEY не настроен."
        )

    url = (
        "https://generativelanguage.googleapis.com"
        f"/v1beta/models/{GEMINI_MODEL}"
        f":generateContent?key={GEMINI_API_KEY}"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Ты полезный AI-помощник "
                            "в Telegram.\n"
                            "Отвечай на русском языке, "
                            "понятно и по делу.\n"
                            "Если вопрос связан с "
                            "программированием — "
                            "приводи примеры.\n\n"
                            f"Вопрос пользователя:\n{prompt}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 1200,
        },
    }

    async with httpx.AsyncClient(
        timeout=45
    ) as client:

        response = await client.post(
            url,
            json=payload
        )

    if response.status_code != 200:

        print(
            "GEMINI ERROR:",
            response.status_code,
            response.text
        )

        return (
            "❌ Gemini не смог обработать "
            "запрос."
        )

    data = response.json()

    try:

        return (
            data["candidates"][0]
            ["content"]["parts"][0]["text"]
        )

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        print(
            "BAD GEMINI RESPONSE:",
            data
        )

        return (
            "❌ Gemini вернул "
            "неожиданный ответ."
        )


@router.message(F.text)
async def text_handler(message: Message):

    prompt = message.text.strip()

    if not prompt:
        return

    wait_message = await message.answer(
        "🤔 Думаю..."
    )

    try:

        answer = await ask_gemini(prompt)

        await wait_message.edit_text(
            answer
        )

    except Exception as e:

        print(
            "HANDLER ERROR:",
            repr(e)
        )

        await wait_message.edit_text(
            "❌ Произошла ошибка."
        )