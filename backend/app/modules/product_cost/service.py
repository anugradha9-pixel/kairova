from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.modules.product.repository import ProductRepository
from app.modules.product_cost.models import ProductCost
from app.modules.product_cost.repository import ProductCostRepository
from app.modules.product_cost.schemas import (
    ProductCostCreate,
    ProductCostUpdate,
)


# =========================================================
# CREATE / UPDATE COST ACCESS CHECK
# =========================================================

def verify_cost_access(product, current_user: User):

    if current_user.is_admin:
        return

    if product.creator.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )


# =========================================================
# CREATE COST
# =========================================================

def create_cost_service(
    db: Session,
    product_id: int,
    payload: ProductCostCreate,
    current_user: User,
):

    product_repo = ProductRepository(db)
    cost_repo = ProductCostRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    verify_cost_access(product, current_user)

    cost = ProductCost(
        product_id=product_id,
        material_cost=payload.material_cost,
        labor_hours=payload.labor_hours,
        labor_rate=payload.labor_rate,
        packaging_cost=payload.packaging_cost,
        shipping_cost=payload.shipping_cost,
        platform_fee_percent=payload.platform_fee_percent or 0.0,
    )

    cost = cost_repo.create(cost)

    db.commit()
    db.refresh(cost)

    return cost


# =========================================================
# GET COST
# =========================================================

def get_cost_service(db: Session, product_id: int):

    repo = ProductCostRepository(db)

    return repo.get_by_product(product_id)


# =========================================================
# UPDATE COST
# =========================================================

def update_cost_service(
    db: Session,
    product_id: int,
    payload: ProductCostUpdate,
    current_user: User,
):

    product_repo = ProductRepository(db)
    cost_repo = ProductCostRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    verify_cost_access(product, current_user)

    cost = cost_repo.get_by_product(product_id)

    if not cost:
        raise HTTPException(
            status_code=404,
            detail="Cost profile not found",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for k, v in update_data.items():
        setattr(cost, k, v)

    cost = cost_repo.update_cost(cost)

    db.commit()
    db.refresh(cost)

    return cost