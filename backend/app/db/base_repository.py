from typing import Generic, Optional, Type, TypeVar

from sqlalchemy.orm import Session

from app.db.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


# =========================================================
# BASE REPOSITORY
# =========================================================

class BaseRepository(Generic[ModelType]):
    """
    Generic base repository for database operations.
    """

    def __init__(
        self,
        db: Session,
        model: Type[ModelType],
    ):
        self.db = db
        self.model = model

    # =====================================================
    # CREATE
    # =====================================================

    def add(
        self,
        obj: ModelType,
    ) -> ModelType:
        """
        Add object to database session.
        """

        self.db.add(obj)

        self.db.flush()

        return obj

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        obj: ModelType,
    ) -> ModelType:
        """
        Update existing object.
        """

        self.db.add(obj)

        self.db.flush()

        return obj

    # =====================================================
    # GET BY ID
    # =====================================================

    def get_by_id(
        self,
        id: int,
    ) -> Optional[ModelType]:
        """
        Retrieve object by primary key.
        """

        return self.db.get(
            self.model,
            id,
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete(
        self,
        obj: ModelType,
    ) -> None:
        """
        Delete object from database.
        """

        self.db.delete(obj)

        self.db.flush()