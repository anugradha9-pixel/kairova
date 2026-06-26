from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.db.base import Base


# =========================================================
# CREATOR MODEL
# =========================================================

class Creator(Base):

    __tablename__ = "creators"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # =====================================================
    # OWNER
    # =====================================================

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    owner = relationship(
        "User",
        back_populates="creators",
    )

    # =====================================================
    # CORE PROFILE INFO
    # =====================================================

    name = Column(
        String(255),
        nullable=False,
        index=True,
    )

    platform = Column(
        String(50),
        nullable=False,
        index=True,
    )

    niche = Column(
        String(100),
        nullable=False,
        index=True,
    )

    # =====================================================
    # AUDIENCE METRICS
    # =====================================================

    followers = Column(
        Integer,
        nullable=False,
        default=0,
    )

    engagement_rate = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    # =====================================================
    # PRICING OUTPUT
    # =====================================================

    estimated_price = Column(
        Float,
        nullable=True,
    )


# =========================================================
# DB INDEXES
# =========================================================

Index(
    "idx_creator_platform",
    Creator.platform,
)

Index(
    "idx_creator_niche",
    Creator.niche,
)

Index(
    "idx_creator_followers",
    Creator.followers,
)