from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    # =====================================
    # PRIMARY KEY
    # =====================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    # =====================================
    # AUTH FIELDS
    # =====================================

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String,
        nullable=False,
    )

    # =====================================
    # TIMESTAMPS
    # =====================================

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    last_login_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =====================================
    # DEBUG / DEV REPRESENTATION
    # =====================================

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"