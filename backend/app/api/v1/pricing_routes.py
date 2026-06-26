from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.pricing.service import calculate_product_price_service

router = APIRouter(prefix="/api/v1/pricing", tags=["Pricing"])


@router.get("/{product_id}")
def get_pricing(product_id: int, db: Session = Depends(get_db)):
    return calculate_product_price_service(db, product_id)