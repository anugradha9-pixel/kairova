# backend/db/imports.py

# Import Base first (important)
from backend.db.models import Base

# Import ALL models here (single source of truth)
from backend.auth import models as auth_models
from backend.creator import models as creator_models


# Optional: exposes Base for Alembic
__all__ = ["Base"]