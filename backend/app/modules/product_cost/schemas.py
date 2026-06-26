from pydantic import BaseModel, ConfigDict
from typing import Optional


# =========================================================
# CREATE
# =========================================================

class ProductCostCreate(BaseModel):
    material_cost: float
    labor_hours: float
    labor_rate: float
    packaging_cost: float
    shipping_cost: float
    platform_fee_percent: Optional[float] = 0.0


# =========================================================
# UPDATE
# =========================================================

class ProductCostUpdate(BaseModel):
    material_cost: Optional[float] = None
    labor_hours: Optional[float] = None
    labor_rate: Optional[float] = None
    packaging_cost: Optional[float] = None
    shipping_cost: Optional[float] = None
    platform_fee_percent: Optional[float] = None


# =========================================================
# RESPONSE
# =========================================================

class ProductCostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int

    material_cost: float
    labor_hours: float
    labor_rate: float
    packaging_cost: float
    shipping_cost: float
    platform_fee_percent: float

    created_at: str
    updated_at: str