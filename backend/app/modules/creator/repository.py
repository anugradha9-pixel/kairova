from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.creator.models import Creator


# =========================================================
# CREATOR REPOSITORY
# =========================================================

class CreatorRepository(BaseRepository[Creator]):
    """
    Repository layer for Creator entity.
    Responsible only for database access.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        super().__init__(
            db=db,
            model=Creator,
        )

    # =====================================================
    # CREATE
    # =====================================================

    def create(
        self,
        creator: Creator,
    ) -> Creator:

        return self.add(
            creator,
        )

    # =====================================================
    # READ
    # =====================================================

    def get_by_id(
        self,
        creator_id: int,
    ) -> Creator | None:

        return (
            self.db.query(Creator)
            .filter(Creator.id == creator_id)
            .first()
        )

    def get_by_user(
        self,
        user_id: int,
    ) -> list[Creator]:

        return (
            self.db.query(Creator)
            .filter(Creator.user_id == user_id)
            .all()
        )

    def get_all(
        self,
    ) -> list[Creator]:

        return (
            self.db.query(Creator)
            .all()
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update_creator(
        self,
        creator: Creator,
    ) -> Creator:

        return self.update(
            creator,
        )

    def update_price(
        self,
        creator: Creator,
        estimated_price: float,
    ) -> Creator:

        creator.estimated_price = estimated_price

        return self.update(
            creator,
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_creator(
        self,
        creator: Creator,
    ) -> None:

        self.delete(
            creator,
        )