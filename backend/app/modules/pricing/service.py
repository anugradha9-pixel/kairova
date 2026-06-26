from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.product.repository import ProductRepository
from app.modules.product_cost.repository import ProductCostRepository


# =========================================================
# PRICING CALCULATION ENGINE
# =========================================================

def calculate_product_price_service(
    db: Session,
    product_id: int,
):

    product_repo = ProductRepository(db)
    cost_repo = ProductCostRepository(db)

    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    cost = cost_repo.get_by_product(product_id)

    if not cost:
        raise HTTPException(
            status_code=404,
            detail="Cost profile not found",
        )

    # =====================================================
    # STEP 1: LABOR COST
    # =====================================================
    labor_cost = cost.labor_hours * cost.labor_rate

    # =====================================================
    # STEP 2: TOTAL COST
    # =====================================================
    total_cost = (
        cost.material_cost
        + labor_cost
        + cost.packaging_cost
        + cost.shipping_cost
    )

    # =====================================================
    # STEP 3: BREAK EVEN PRICE
    # =====================================================
    break_even_price = total_cost

    # =====================================================
    # STEP 4: RECOMMENDED PRICE
    # =====================================================
    target_margin = 40  # MVP fixed margin (can evolve later)

    recommended_price = total_cost / (1 - target_margin / 100)

    # =====================================================
    # STEP 5: PROFIT
    # =====================================================
    profit_amount = recommended_price - total_cost

    # =====================================================
    # STEP 6: PROFIT MARGIN
    # =====================================================
    profit_margin = (profit_amount / recommended_price) * 100

    return {
        "product_id": product_id,
        "product_name": product.name,

        "total_cost": round(total_cost, 2),
        "break_even_price": round(break_even_price, 2),
        "recommended_price": round(recommended_price, 2),
        "profit_amount": round(profit_amount, 2),
        "profit_margin": round(profit_margin, 2),
    }