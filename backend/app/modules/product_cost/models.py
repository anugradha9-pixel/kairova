from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin


class ProductCost(Base, TimestampMixin):
    __tablename__ = "product_costs"

    # =====================================
    # PRIMARY KEY
    # =====================================
    id = Column(Integer, primary_key=True, index=True)

    # =====================================
    # PRODUCT RELATIONSHIP
    # =====================================
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    product = relationship(
        "Product",
        backref="cost",
    )

    # =====================================
    # COST STRUCTURE
    # =====================================
    material_cost = Column(Float, nullable=False)
    labor_hours = Column(Float, nullable=False)
    labor_rate = Column(Float, nullable=False)

    packaging_cost = Column(Float, nullable=False)
    shipping_cost = Column(Float, nullable=False)

    platform_fee_percent = Column(Float, nullable=True, default=0.0)