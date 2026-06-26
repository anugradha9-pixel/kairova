from sqlalchemy.orm import Session

from app.db.base_repository import BaseRepository
from app.modules.product.models import Product


class ProductRepository(BaseRepository[Product]):

    def __init__(self, db: Session):
        super().__init__(db=db, model=Product)

    # =====================================
    # CREATE
    # =====================================

    def create(self, product: Product) -> Product:
        return self.add(product)

    # =====================================
    # READ
    # =====================================

    def get_by_id(self, product_id: int) -> Product | None:
        return (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def get_all(self) -> list[Product]:
        return self.db.query(Product).all()

    def get_by_creator(self, creator_id: int) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.creator_id == creator_id)
            .all()
        )

    # =====================================
    # UPDATE
    # =====================================

    def update_product(self, product: Product) -> Product:
        return self.update(product)

    # =====================================
    # DELETE
    # =====================================

    def delete_product(self, product: Product) -> None:
        self.delete(product)