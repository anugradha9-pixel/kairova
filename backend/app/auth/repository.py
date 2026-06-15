from sqlalchemy.orm import Session

from app.auth.models import User


class AuthRepository:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

    # =====================================
    # GET USER BY EMAIL
    # =====================================

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    # =====================================
    # GET USER BY ID
    # =====================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # =====================================
    # CREATE USER
    # =====================================

    def create_user(
        self,
        user_data: dict,
    ) -> User:

        user = User(**user_data)

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        return user

    # =====================================
    # UPDATE USER
    # =====================================

    def update_user(
        self,
        user: User,
        updates: dict,
    ) -> User:

        for field, value in updates.items():

            setattr(
                user,
                field,
                value,
            )

        self.db.commit()

        self.db.refresh(user)

        return user

    # =====================================
    # DELETE USER
    # =====================================

    def delete_user(
        self,
        user: User,
    ) -> None:

        self.db.delete(user)

        self.db.commit()