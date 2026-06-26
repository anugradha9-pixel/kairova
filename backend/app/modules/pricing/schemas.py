from pydantic import BaseModel


class PricingResponse(BaseModel):
    product_id: int
    product_name: str

    total_cost: float
    break_even_price: float
    recommended_price: float
    profit_amount: float
    profit_margin: float