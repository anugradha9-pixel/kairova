from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.creator.models import Creator


# =========================================================
# CREATOR REPOSITORY
# =========================================================

class CreatorRepository(BaseRepository):
    """
    Repository layer for Creator entity.
    Responsible only for database access.
    """

    def __init__(self, db: Session):
        super().__init__(db, Creator)

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        creator: Creator,
    ) -> Creator:

        return self.add(creator)

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        creator_id: int,
    ) -> Creator | None:

        result = self.db.execute(
            select(Creator).where(
                Creator.id == creator_id
            )
        )

        return result.scalar_one_or_none()

    # =====================================================
    # UPDATE PRICE
    # =====================================================

    def update_price(
        self,
        creator: Creator,
        estimated_price: float,
    ) -> Creator:

        creator.estimated_price = estimated_price

        return self.update(creator)