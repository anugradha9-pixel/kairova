from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.config.settings import settings


# =====================================
# DATABASE URL
# =====================================

DATABASE_URL = settings.DATABASE_URL

if "sqlite" in DATABASE_URL:
    raise RuntimeError(
        f"SQLite detected in DATABASE_URL: {DATABASE_URL}"
    )


# =====================================
# ENGINE
# =====================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)


# =====================================
# SESSION FACTORY
# =====================================

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# =====================================
# DATABASE DEPENDENCY
# =====================================

def get_db():
    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()