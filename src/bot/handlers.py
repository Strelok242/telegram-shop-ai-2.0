from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .keyboards import main_menu_kb

from src.db.database import async_session
from src.db.crud import list_products

from src.bot.keyboards import product_add_kb
from src.db.crud import add_to_cart, get_cart



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

    async with async_session() as session:
        products = await list_products(session)

    if not products:
        await callback.message.answer("Каталог пуст.")
        return

    await callback.message.answer("Каталог товаров:")

    for p in products:
        price = p.price_cents / 100
        text = f"• {p.title}\nЦена: {price:.2f} ₽\n{p.description or ''}".strip()
        await callback.message.answer(text, reply_markup=product_add_kb(p.id))




@router.callback_query(F.data == "menu:cart")
async def on_cart(callback: CallbackQuery) -> None:
    await callback.answer()
    user_id = callback.from_user.id

    async with async_session() as session:
        items = await get_cart(session, user_id=user_id)

    if not items:
        await callback.message.answer("Корзина пуста.")
        return

    total_cents = 0
    lines = ["Корзина:"]
    for it in items:
        price = it.product.price_cents
        total_cents += price * it.qty
        lines.append(f"• {it.product.title} × {it.qty} — {(price * it.qty)/100:.2f} ₽")

    lines.append(f"\nИтого: {total_cents/100:.2f} ₽")
    await callback.message.answer("\n".join(lines))



@router.callback_query(F.data == "menu:help")
async def on_help(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.answer("Помощь: /start — открыть меню.")

@router.callback_query(F.data.startswith("cart:add:"))
async def on_add_to_cart(callback: CallbackQuery) -> None:
    await callback.answer()

    product_id = int(callback.data.split(":")[-1])
    user_id = callback.from_user.id

    async with async_session() as session:
        await add_to_cart(session, user_id=user_id, product_id=product_id, qty=1)

    await callback.message.answer("Добавлено в корзину.")

