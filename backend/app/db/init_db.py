import os

from app.db.base import Base
from app.db.session import engine

# =========================================================
# IMPORT MODEL REGISTRY
# =========================================================
# IMPORTANT:
# This ensures SQLAlchemy registers all ORM models
# before create_all() executes.
# =========================================================

from app.db import imports  # noqa: F401


# =========================================================
# INITIAL DATABASE CREATION
# =========================================================

def init_db() -> None:
    """
    Development-only database initialization.

    Creates all database tables directly from
    SQLAlchemy ORM models.

    WARNING:
    Do NOT use in production.
    Use Alembic migrations instead.
    """

    environment = os.getenv(
        "APP_ENV",
        "development",
    ).lower()

    # =====================================================
    # SAFETY CHECK
    # =====================================================

    if environment != "development":
        raise RuntimeError(
            "init_db() is restricted to development mode only."
        )

    # =====================================================
    # CREATE TABLES
    # =====================================================

    Base.metadata.create_all(
        bind=engine,
    )

    # =====================================================
    # SUCCESS LOG
    # =====================================================

    print(
        "✅ Database tables created successfully"
    )