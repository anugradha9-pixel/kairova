from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "products"

    # =====================================
    # PRIMARY KEY
    # =====================================
    id = Column(Integer, primary_key=True, index=True)

    # =====================================
    # OWNER (CREATOR)
    # =====================================
    creator_id = Column(
        Integer,
        ForeignKey("creators.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    creator = relationship(
        "Creator",
        backref="products",
    )

    # =====================================
    # PRODUCT CORE FIELDS
    # =====================================
    name = Column(String(255), nullable=False, index=True)

    description = Column(Text, nullable=True)