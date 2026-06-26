# =========================================================
# ORM MODEL REGISTRY
# =========================================================
#
# This file exists ONLY to import all ORM models so that:
#
# 1. SQLAlchemy Base.metadata is fully populated
# 2. Alembic autogenerate can detect all tables
# 3. Circular imports are avoided
#
# DO NOT define Base here.
# Base lives in app.db.base
#
# =========================================================

from app.db.base import Base


# =========================================================
# IMPORT ALL ORM MODELS
# =========================================================

from app.auth.models import User  # noqa: F401
from app.auth.session_models import UserSession  # noqa: F401

from app.modules.creator.models import Creator  # noqa: F401

from app.modules.product.models import Product  # noqa: F401
from app.modules.product_cost.models import ProductCost  # noqa: F401


# =========================================================
# FUTURE MODULES
# =========================================================

# from app.billing.models import Subscription
# from app.analytics.models import Event
# from app.marketplace.models import Campaign


# =========================================================
# EXPORTS
# =========================================================

__all__ = [
    "Base",
]