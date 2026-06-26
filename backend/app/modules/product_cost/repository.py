from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.product_cost.models import ProductCost


class ProductCostRepository(BaseRepository[ProductCost]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=ProductCost)

    # =====================================
    # CREATE
    # =====================================

    def create(self, cost: ProductCost) -> ProductCost:
        return self.add(cost)

    # =====================================
    # READ
    # =====================================

    def get_by_id(self, cost_id: int) -> ProductCost | None:
        return (
            self.db.query(ProductCost)
            .filter(ProductCost.id == cost_id)
            .first()
        )

    def get_by_product(self, product_id: int) -> ProductCost | None:
        return (
            self.db.query(ProductCost)
            .filter(ProductCost.product_id == product_id)
            .first()
        )

    # =====================================
    # UPDATE
    # =====================================

    def update_cost(self, cost: ProductCost) -> ProductCost:
        return self.update(cost)

    # =====================================
    # DELETE
    # =====================================

    def delete_cost(self, cost: ProductCost) -> None:
        self.delete(cost)