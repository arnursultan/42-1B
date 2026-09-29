from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import db

router = Router()


def servers_keyboard():
    buttons = [
        [InlineKeyboardButton(text=f"🖥 {s['name']}", callback_data=f"server:{s['name']}")]
        for s in db.get_all_servers()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Сап, {message.from_user.first_name}! 👋\n"
        "Я дежурный Серверной комнаты. Теперь живу в облаке, но проблемы всё те же.\n\n"
        "/servers — выбрать сервер кнопкой\n"
        "/list — список всех серверов\n"
        "/incidents — инциденты (JOIN двух таблиц)\n"
        "/stats — статистика по статусам (GROUP BY)"
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    lines = [f"• {s['name']} ({s['type']}) — {s['status']}" for s in db.get_all_servers()]
    await message.answer("Серверы в реестре:\n" + "\n".join(lines))


@router.message(Command("servers"))
async def cmd_servers(message: Message):
    await message.answer("Выбери сервер для диагностики:", reply_markup=servers_keyboard())


@router.callback_query(F.data.startswith("server:"))
async def cb_server(callback: CallbackQuery):
    name = callback.data.split(":", 1)[1]
    server = db.get_server_by_name(name)
    if server is None:
        await callback.message.edit_text("Сервер пропал из реестра. Мистика.")
    else:
        await callback.message.edit_text(
            f"🖥 {server['name']}\nТип: {server['type']}\nСтатус: {server['status']}"
        )
    await callback.answer()


@router.message(Command("incidents"))
async def cmd_incidents(message: Message):
    rows = db.get_incidents()
    if not rows:
        await message.answer("Инцидентов нет. Подозрительно.")
        return
    lines = [f"🔥 {r['server']}: {r['description']}" for r in rows]
    await message.answer("Журнал инцидентов:\n" + "\n".join(lines))


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    lines = [f"{r['status']}: {r['total']}" for r in db.get_stats()]
    await message.answer("Статистика по статусам:\n" + "\n".join(lines))


@router.message()
async def fallback(message: Message):
    await message.answer("Не понял. Наберите /start — я не телепат, я бот в облаке.")