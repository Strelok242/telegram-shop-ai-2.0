from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(text="Каталог", callback_data="menu:catalog"),
        InlineKeyboardButton(text="Корзина", callback_data="menu:cart"),
    )
    kb.add(
        InlineKeyboardButton(text="Помощь", callback_data="menu:help"),
    )
    kb.adjust(2, 1)
    return kb.as_markup()

def product_add_kb(product_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Добавить в корзину", callback_data=f"cart:add:{product_id}"))
    return kb.as_markup()
