from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


async def list_products(session: AsyncSession) -> list[Product]:
    res = await session.execute(select(Product).order_by(Product.id))
    return list(res.scalars().all())
