from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


async def list_products(session: AsyncSession) -> list[Product]:
    res = await session.execute(select(Product).order_by(Product.id))
    return list(res.scalars().all())

from sqlalchemy import delete
from sqlalchemy.orm import selectinload

from .models import CartItem, Product


async def add_to_cart(session: AsyncSession, user_id: int, product_id: int, qty: int = 1) -> None:
    # если уже есть — увеличиваем qty
    res = await session.execute(
        select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == product_id)
    )
    item = res.scalar_one_or_none()
    if item:
        item.qty += qty
    else:
        session.add(CartItem(user_id=user_id, product_id=product_id, qty=qty))
    await session.commit()


async def get_cart(session: AsyncSession, user_id: int) -> list[CartItem]:
    res = await session.execute(
        select(CartItem)
        .options(selectinload(CartItem.product))
        .where(CartItem.user_id == user_id)
        .order_by(CartItem.id)
    )
    return list(res.scalars().all())


async def clear_cart(session: AsyncSession, user_id: int) -> None:
    await session.execute(delete(CartItem).where(CartItem.user_id == user_id))
    await session.commit()
