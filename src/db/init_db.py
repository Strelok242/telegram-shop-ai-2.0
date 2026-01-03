from __future__ import annotations

from sqlalchemy import func, select

from .database import engine, async_session
from .models import Base, Product


async def init_db() -> None:
    # создать таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # сидинг (если пусто)
    async with async_session() as session:
        count_res = await session.execute(select(func.count(Product.id)))
        count = int(count_res.scalar() or 0)

        if count == 0:
            session.add_all(
                [
                    Product(
                        title="Серебряный меч (сувенир)",
                        price_cents=199900,
                        description="Для монстров и для понтов. Не для школы.",
                    ),
                    Product(
                        title="Масло против утопцев",
                        price_cents=49900,
                        description="Повышает эффективность против водных гадов.",
                    ),
                    Product(
                        title="Зелье 'Кошка'",
                        price_cents=29900,
                        description="Улучшает зрение в темноте. Не мешать с самоуверенностью.",
                    ),
                ]
            )
            await session.commit()
