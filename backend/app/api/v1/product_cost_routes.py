from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

from app.modules.product_cost.schemas import (
    ProductCostCreate,
    ProductCostUpdate,
)
from app.modules.product_cost.service import (
    create_cost_service,
    get_cost_service,
    update_cost_service,
)

router = APIRouter(prefix="/api/v1/products", tags=["Product Costs"])


@router.post("/{product_id}/costs")
def create_cost(
    product_id: int,
    payload: ProductCostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_cost_service(db, product_id, payload, current_user)


@router.get("/{product_id}/costs")
def get_cost(product_id: int, db: Session = Depends(get_db)):
    return get_cost_service(db, product_id)


@router.put("/{product_id}/costs")
def update_cost(
    product_id: int,
    payload: ProductCostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_cost_service(db, product_id, payload, current_user)