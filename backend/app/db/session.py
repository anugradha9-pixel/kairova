from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.settings import settings


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL: str = settings.DATABASE_URL

if "sqlite" in DATABASE_URL.lower():
    raise RuntimeError(
        "SQLite is not supported for MakerMint backend."
    )


# =========================================================
# SQLALCHEMY ENGINE
# =========================================================
# NOTE:
# pool_pre_ping prevents stale DB connections
# pool_recycle avoids timeout issues in production

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    future=True,
    echo=False,  # set True for SQL debugging only
)


# =========================================================
# SESSION FACTORY
# =========================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


# =========================================================
# DATABASE DEPENDENCY (FASTAPI)
# =========================================================

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a SQLAlchemy session.

    Ensures:
    - Proper session lifecycle
    - Automatic cleanup after request
    """

    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()