from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.creator.models import Creator


# =========================================================
# CREATOR REPOSITORY
# =========================================================

class CreatorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================

    async def create(self, creator: Creator) -> Creator:
        self.db.add(creator)

        await self.db.commit()
        await self.db.refresh(creator)

        return creator

    # =====================================================
    # READ
    # =====================================================

    async def get_by_id(
        self,
        creator_id: int,
    ) -> Creator | None:

        result = await self.db.execute(
            select(Creator).where(
                Creator.id == creator_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================

    async def update(
        self,
        creator: Creator,
    ) -> Creator:

        self.db.add(creator)

        await self.db.commit()
        await self.db.refresh(creator)

        return creator

    # =====================================================
    # UPDATE PRICE
    # =====================================================

    async def update_price(
        self,
        creator: Creator,
        estimated_price: float,
    ) -> Creator:

        creator.estimated_price = estimated_price

        return await self.update(creator)