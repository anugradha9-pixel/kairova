# =========================================================
# SQLALCHEMY MODEL REGISTRY
# =========================================================
# Central import registry for:
# - Alembic metadata discovery
# - ORM model registration
# - Future relationship loading
#
# IMPORTANT:
# Do NOT remove these imports.
# Alembic relies on them to detect models.
# =========================================================


# =========================================================
# BASE METADATA
# =========================================================

from app.db.base import Base


# =========================================================
# AUTH MODELS
# =========================================================

from app.auth.models import User  # noqa: F401


# =========================================================
# CREATOR MODELS
# =========================================================

from app.creator.models import Creator  # noqa: F401


# =========================================================
# FUTURE DOMAIN MODELS
# =========================================================
# Add future ORM models here:
#
# from app.billing.models import Subscription
# from app.analytics.models import AnalyticsEvent
# from app.share.models import SharedReport
#
# Keep imports explicit for Alembic safety.
# =========================================================


# =========================================================
# EXPORTS
# =========================================================

__all__ = [
    "Base",
]