from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .keyboards import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот магазина.\n"
        "Пока это прототип: каталог/корзина будут заглушками, дальше подключим БД и WebApp.",
        reply_markup=main_menu_kb(),
    )


@router.callback_query(F.data == "menu:catalog")
async def on_catalog(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Каталог: пока заглушка. Дальше подключим базу и товары.")


@router.callback_query(F.data == "menu:cart")
async def on_cart(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Корзина: пока пусто. Дальше добавим логику корзины.")


@router.callback_query(F.data == "menu:help")
async def on_help(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Помощь: /start — открыть меню.")
