from sqlalchemy.orm import Session

from app.auth.models import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================
    # GET USER
    # =====================================

    def get_by_id(
        self,
        user_id: int,
    ):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # =====================================
    # LIST USERS
    # =====================================

    def get_all(self):

        return (
            self.db.query(User)
            .order_by(User.id)
            .all()
        )

    # =====================================
    # UPDATE USER
    # =====================================

    def save(
        self,
        user: User,
    ):

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # =====================================
    # DELETE USER
    # =====================================

    def delete(
        self,
        user: User,
    ):

        self.db.delete(user)
        self.db.commit()