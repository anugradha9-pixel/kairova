from sqlalchemy import Column, Float, Integer, String, Index

from app.db.base import Base


# =========================================================
# CREATOR MODEL
# =========================================================

class Creator(Base):
    """
    ORM model representing a content creator
    in the MakerMint system.
    """

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
# DB INDEXES (PERFORMANCE OPTIMIZATION)
# =========================================================

Index("idx_creator_platform", Creator.platform)
Index("idx_creator_niche", Creator.niche)
Index("idx_creator_followers", Creator.followers)