import os
from backend.db.models import Base
from backend.db.session import engine

# IMPORT ALL MODELS (ENSURE TABLE REGISTRATION)
from backend.auth.models import User  # noqa
from backend.creator.models import Creator  # noqa


def init_db():
    """
    DEV ONLY:
    Creates all tables directly from SQLAlchemy models.
    DO NOT USE IN PRODUCTION (use Alembic instead).
    """

    if os.getenv("ENV", "development") != "development":
        raise RuntimeError("init_db() is only allowed in development mode")

    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")