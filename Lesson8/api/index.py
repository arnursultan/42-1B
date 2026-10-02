import os
import traceback

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from bot.handlers import router


app = FastAPI()

dp = Dispatcher()
dp.include_router(router)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "Telegram bot is running"
    }


@app.post("/api/webhook")
async def webhook(request: Request):

    print("Webhook start")

    try:
        token = os.getenv("BOT_TOKEN")

        if not token:
            print("BOT_TOKEN IS MISSING")
            return {
                "ok": False,
                "error": "BOT_TOKEN is missing"
            }

        print("BOT_TOKEN: OK")

        data = await request.json()

        print("UPDATE RECEIVED")

        bot = Bot(token=token)

        try:
            update = Update.model_validate(
                data,
                context={"bot": bot}
            )

            print(
                "UPDATE TYPE:",
                update.event_type
            )

            await dp.feed_update(
                bot,
                update
            )

            print("UPDATE PROCESSED")

        finally:
            await bot.session.close()

        print("Webhook Success")

        return {
            "ok": True
        }

    except Exception as e:

        print("Webhook Error")
        print(repr(e))
        traceback.print_exc()

        return {
            "ok": False,
            "error": repr(e)
        }