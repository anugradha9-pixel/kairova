from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.creator.models import Creator


class CreatorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    # =====================================================
    # CREATE
    # =====================================================
    async def create_creator(self, creator: Creator) -> Creator:
        self.db.add(creator)
        await self.db.commit()
        await self.db.refresh(creator)
        return creator

    # =====================================================
    # READ
    # =====================================================
    async def get_by_id(self, creator_id: int) -> Creator | None:
        result = await self.db.execute(
            select(Creator).where(Creator.id == creator_id)
        )
        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE
    # =====================================================
    async def update_creator(self, creator: Creator) -> Creator:
        self.db.add(creator)
        await self.db.commit()
        await self.db.refresh(creator)
        return creator