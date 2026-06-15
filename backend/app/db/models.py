# =========================================================
# ORM MODEL REGISTRY (LEGACY COMPATIBILITY LAYER)
# =========================================================
# IMPORTANT:
# Base is defined in app.db.base
# This file is ONLY for model aggregation (NOT Base definition)
# =========================================================


from app.db.base import Base  # re-export for legacy imports compatibility


# =========================================================
# IMPORT ALL ORM MODELS
# =========================================================
# Ensures SQLAlchemy metadata is populated

from app.auth.models import User  # noqa: F401
from app.modules.creator.models import Creator  # noqa: F401


# =========================================================
# OPTIONAL FUTURE MODELS
# =========================================================
# from app.billing.models import Subscription
# from app.analytics.models import Event


# =========================================================
# EXPORTS
# =========================================================

__all__ = ["Base"]