from datetime import (
    datetime,
    timezone,
)

from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.session_models import UserSession


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AuthRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================
    # USERS
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

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def create_user(
        self,
        user_data: dict,
    ) -> User:

        user = User(**user_data)

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise

    def update_user(
        self,
        user: User,
        updates: dict,
    ) -> User:

        try:
            for field, value in updates.items():
                setattr(user, field, value)

            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise

    def delete_user(
        self,
        user: User,
    ) -> None:

        try:
            self.db.delete(user)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    # =====================================
    # SESSIONS
    # =====================================

    def create_session(
        self,
        user_id: int,
        session_id: str,
        refresh_jti: str,
        expires_at: datetime,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> UserSession:

        session = UserSession(
            user_id=user_id,
            session_id=session_id,
            refresh_jti=refresh_jti,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            is_active=True,
        )

        try:
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

            return session

        except Exception:
            self.db.rollback()
            raise

    def get_session_by_id(
        self,
        session_pk: int,
    ) -> UserSession | None:

        return (
            self.db.query(UserSession)
            .filter(UserSession.id == session_pk)
            .first()
        )

    def get_session_by_jti(
        self,
        refresh_jti: str,
    ) -> UserSession | None:

        return (
            self.db.query(UserSession)
            .filter(
                UserSession.refresh_jti == refresh_jti,
                UserSession.is_active.is_(True),
                UserSession.expires_at >= utc_now(),
            )
            .first()
        )

    def get_session_by_session_id(
        self,
        session_id: str,
    ) -> UserSession | None:

        return (
            self.db.query(UserSession)
            .filter(
                UserSession.session_id == session_id,
                UserSession.is_active.is_(True),
                UserSession.expires_at >= utc_now(),
            )
            .first()
        )

    def rotate_session_jti(
        self,
        session: UserSession,
        new_jti: str,
    ) -> UserSession:

        try:
            session.refresh_jti = new_jti

            self.db.commit()
            self.db.refresh(session)

            return session

        except Exception:
            self.db.rollback()
            raise

    def revoke_session(
        self,
        session_id: int,
    ) -> None:

        session = self.get_session_by_id(
            session_id
        )

        if not session:
            return

        try:
            session.is_active = False

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def revoke_all_user_sessions(
        self,
        user_id: int,
    ) -> None:

        try:
            (
                self.db.query(UserSession)
                .filter(UserSession.user_id == user_id)
                .update(
                    {
                        "is_active": False,
                    },
                    synchronize_session=False,
                )
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def revoke_oldest_active_session(
        self,
        user_id: int,
    ) -> None:

        oldest = (
            self.db.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.is_active.is_(True),
                UserSession.expires_at >= utc_now(),
            )
            .order_by(UserSession.created_at.asc())
            .first()
        )

        if not oldest:
            return

        try:
            oldest.is_active = False

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def get_user_active_sessions(
        self,
        user_id: int,
    ) -> list[UserSession]:

        return (
            self.db.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.is_active.is_(True),
                UserSession.expires_at >= utc_now(),
            )
            .order_by(UserSession.created_at.desc())
            .all()
        )

    def count_user_active_sessions(
        self,
        user_id: int,
    ) -> int:

        return (
            self.db.query(UserSession)
            .filter(
                UserSession.user_id == user_id,
                UserSession.is_active.is_(True),
                UserSession.expires_at >= utc_now(),
            )
            .count()
        )

    def cleanup_expired_sessions(
        self,
    ) -> int:

        try:
            deleted = (
                self.db.query(UserSession)
                .filter(
                    UserSession.expires_at <= utc_now()
                )
                .delete(
                    synchronize_session=False
                )
            )

            self.db.commit()

            return deleted

        except Exception:
            self.db.rollback()
            raise