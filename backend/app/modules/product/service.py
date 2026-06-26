from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.auth.models import User
from app.modules.creator.repository import CreatorRepository
from app.modules.product.models import Product
from app.modules.product.repository import ProductRepository
from app.modules.product.schemas import ProductCreate, ProductUpdate


# =========================================================
# OWNERSHIP CHECK
# =========================================================

def verify_product_access(product: Product, current_user: User):

    if current_user.is_admin:
        return

    if product.creator.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )


# =========================================================
# CREATE PRODUCT
# =========================================================

def create_product_service(
    db: Session,
    payload: ProductCreate,
    current_user: User,
):

    creator_repo = CreatorRepository(db)
    product_repo = ProductRepository(db)

    creator = creator_repo.get_by_id(payload.creator_id)

    if not creator:
        raise HTTPException(
            status_code=404,
            detail="Creator not found",
        )

    if not current_user.is_admin and creator.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not your creator profile",
        )

    product = Product(
        creator_id=payload.creator_id,
        name=payload.name,
        description=payload.description,
    )

    product = product_repo.create(product)

    db.commit()
    db.refresh(product)

    return product


# =========================================================
# GET PRODUCT BY ID
# =========================================================

def get_product_by_id_service(db: Session, product_id: int):

    repo = ProductRepository(db)

    return repo.get_by_id(product_id)


# =========================================================
# GET PRODUCTS BY CREATOR
# =========================================================

def get_products_service(db: Session, creator_id: int):

    repo = ProductRepository(db)

    return repo.get_by_creator(creator_id)


# =========================================================
# UPDATE PRODUCT
# =========================================================

def update_product_service(
    db: Session,
    product_id: int,
    payload: ProductUpdate,
    current_user: User,
):

    repo = ProductRepository(db)

    product = repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    verify_product_access(product, current_user)

    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    product = repo.update_product(product)

    db.commit()
    db.refresh(product)

    return product


# =========================================================
# DELETE PRODUCT
# =========================================================

def delete_product_service(
    db: Session,
    product_id: int,
    current_user: User,
):

    repo = ProductRepository(db)

    product = repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    verify_product_access(product, current_user)

    repo.delete_product(product)

    db.commit()

    return {"message": "Product deleted successfully"}