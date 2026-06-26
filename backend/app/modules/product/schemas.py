from pydantic import BaseModel, ConfigDict
from typing import Optional


# =========================================================
# PRODUCT CREATE
# =========================================================

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    creator_id: int


# =========================================================
# PRODUCT UPDATE
# =========================================================

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# =========================================================
# PRODUCT RESPONSE
# =========================================================

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int

    name: str
    description: Optional[str]

    created_at: Optional[str]
    updated_at: Optional[str]