from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.auth.models import User

from app.modules.product.schemas import ProductCreate, ProductUpdate
from app.modules.product.service import (
    create_product_service,
    get_product_by_id_service,
    get_products_service,
    update_product_service,
    delete_product_service,
)

router = APIRouter(prefix="/api/v1/products", tags=["Products"])


@router.post("")
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_product_service(db, payload, current_user)


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id_service(db, product_id)


@router.get("")
def get_products(creator_id: int, db: Session = Depends(get_db)):
    return get_products_service(db, creator_id)


@router.put("/{product_id}")
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_product_service(db, product_id, payload, current_user)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_product_service(db, product_id, current_user)