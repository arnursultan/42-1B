# from selectors import SelectorKey
#
# CRUD
# Create - INSERT
# Read - SELECT
# Update - UPDATE
# Delete - DELETE
#
# SELECT * FROM servers — Все столбцы, все строки.
# SELECT name, status FROM servers — только нужные столбцы
# SELECT * FROM servers WHERE status = "мёртв" — фильтр
# SELECT * FROM servers WHERE type != 'web' — не равно
# SELECT * FROM servers WHERE name LIKE '%server%'; — поиск по подстроке
# SELECT * FROM servers WHERE status = 'жив' AND type = 'db' — несколько условий
# SELECT * FROM servers ORDER BY name — сортировка А->Я
# SELECT * FROM servers ORDER BY id DESC — сортировка по убыванию
# SELECT * FROM servers ORDER BY id ASC — сортировка по возрастанию
# ASC — Ascending — Восходящий, от меньшего к большему
# DESC — Descending — Нисходящий, от большего к меньшему
# SELECT * FROM servers LIMIT 2 — только первые 2 строки
#
# UPDATE servers SET status = 'мёртв' WHERE name = 'mail_server'
# UPDATE servers SET status = 'жив', type = 'db' WHERE id = 2
#
# DELETE FROM servers WHERE name = "mail_server"

import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import Lesson5_db

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
router = Router()









