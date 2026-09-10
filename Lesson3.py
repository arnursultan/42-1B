import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Клавиатуры
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статус"),
         KeyboardButton(text="😂 Шутка")],
        [KeyboardButton(text="💻 Серверы"),
         KeyboardButton(text="📞 Помощь")],
    ],
    resize_keyboard=True,
)

servers_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🖥️ web_server", callback_data="server:web")],
    [InlineKeyboardButton(text="💾 db_server", callback_data="server:db")],
    [InlineKeyboardButton(text="📼 backup_server", callback_data="backup:server")],
])

confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Сохранить", callback_data="confirm_save")],
    [InlineKeyboardButton(text="❌ Отмена", callback_data="confirm_cancel")],
])

SERVER_DIAGNOSIS = {
    "web": "🖥️ web_server: нагрузка 14%, всё спокойно.",
    "db": "💾 db_server: 4 соединения зависли, но кто их считает.",
    "backup": "📼 backup_server: молчит 5-й день. Классика.",
}

# FSM - добавление сервера
class AddServerStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_type = State()
    waiting_for_status = State()

# Базовые команды
@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Здравствуйте, {message.from_user.first_name}!👋🏼\n"
        "Я Бот Сервера 42-1B. Вся система пашет, всё нормально.",
        reply_markup=main_keyboard,
    )

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "/start — старт бота; знакомство:\n"
        "/status — статус серверов\n"
        "/joke — шутка от разработчика\n"
        "/servers — диагностика конкретного сервера\n"
        "/add_servers — добавить сервер в реестр\n"
        "/cancel — прервать текущий диалог"
    )

@router.message(Command("status"))
async def status(message: Message):
    await message.answer(
        "🖥️ web_server — жив\n"
        "💾 db_server — жив, но грустит\n"
        "📼 backup_sever — не отвечает, игнор, это база."
    )

@router.message(Command("joke"))
async def joke(message: Message):
    await message.answer(
        "Если вы начинаете сгонять муху с монитора при помощи курсора мыши, пора выключать компьютер"
    )

@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нечего отменять, Добби свободен.")
        return
    await state.clear()
    await message.answer("Диалог отменён. Реестр серверов не тронут.")

# Reply-кнопки
@router.message(F.text == "📊 Статус")
async def button_status(message: Message):
    await status(message)

@router.message(F.text == "😂 Шутка")
async def button_joke(message: Message):
    await joke(message)

@router.message(F.text == "📞 Помощь")
async def button_help(message: Message):
    await help(message)

@router.message(F.text == "💻 Серверы")
async def buttons_servers(message: Message):
    await servers(message)

# Inline кнопки
@router.message(Command("servers"))
async def servers(message: Message):
    await message.answer("Выберите сервер для диагностики:",
                         reply_markup=servers_keyboard)

@router.callback_query(F.data.startswith("server:"))
async def cb_servers_diagnosis(callback: CallbackQuery):
    server_key = callback.data.split(":")[1]
    text = SERVER_DIAGNOSIS.get(server_key, "Неизвестный сервер.")
    await callback.message.edit_text(text)
    await callback.answer()

# FSM-диалог добавление сервера
@router.message(Command("add_server"))
async def add_server(message: Message, state: FSMContext):
    await message.answer("Введите имя нового сервера:")
    await state.set_state(AddServerStates.waiting_for_name)

@router.message(AddServerStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Принято. Теперь тип сервера (web / db / backup):")
    await state.set_state(AddServerStates.waiting_for_type)

@router.message(AddServerStates.waiting_for_type)
async def process_type(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("И последнее — статус (жив / мёртв / в отпуске):")
    await state.set_state(AddServerStates.waiting_for_status)

@router.message(AddServerStates.waiting_for_status)
async def process_status(message: Message, state: FSMContext):
    data = await state.update_data(status=message.text)
    await message.answer(
        "Проверьте данные:\n"
        f"Имя: {data['name']}\n"
        f"Тип: {data['type']}\n"
        f"Статус: {data['status']}",
        reply_markup=confirm_keyboard,
    )

@router.callback_query(F.data == "confirm_save")
async def cb_confirm_save(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Сервер сохранён в реестре ✅")
    await callback.answer()

@router.callback_query(F.data == "confirm_cancel")
async def cb_confirm_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Добавление отменено ❌")
    await callback.answer()

@router.message()
async def echo_all(message: Message):
    await message.answer(
        f"Не понял команду '{message.text}. Наберите /help — по братски."
    )

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



