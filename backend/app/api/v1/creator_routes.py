from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.auth.permissions import require_authenticated
from app.auth.models import User

from app.modules.creator.service import (
    create_creator_service,
    get_creator_pricing_service,
    get_creator_by_id_service,
    get_my_creators_service,
    update_creator_service,
    delete_creator_service,
)

from app.modules.creator.schemas import (
    CreatorCreate,
    CreatorResponse,
    CreatorDTO,
    CreatorListResponse,
    CreatorUpdateRequest,
)

from app.schemas.response import APIResponse


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/creators",
    tags=["Creators"],
)


# =========================================================
# CREATE CREATOR
# =========================================================

@router.post(
    "",
    response_model=CreatorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_creator(
    payload: CreatorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """
    Create creator owned by current user.
    """

    creator = create_creator_service(
        db=db,
        payload=payload,
        current_user=current_user,
    )

    return CreatorResponse.model_validate(
        creator
    )


# =========================================================
# GET MY CREATORS
# =========================================================

@router.get(
    "/mine",
    response_model=CreatorListResponse,
)
def get_my_creators(
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """
    Return creators owned by current user.
    """

    creators = get_my_creators_service(
        db=db,
        current_user=current_user,
    )

    return CreatorListResponse(
        creators=[
            CreatorDTO.model_validate(c)
            for c in creators
        ]
    )


# =========================================================
# GET CREATOR
# =========================================================

@router.get(
    "/{creator_id}",
    response_model=CreatorDTO,
)
def get_creator(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """
    Get creator by ID.
    Owner or admin only.
    """

    creator = get_creator_by_id_service(
        db,
        creator_id,
    )

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found",
        )

    if (
        creator.user_id != current_user.id
        and not current_user.is_admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return CreatorDTO.model_validate(
        creator
    )


# =========================================================
# UPDATE CREATOR
# =========================================================

@router.patch(
    "/{creator_id}",
    response_model=CreatorDTO,
)
def update_creator(
    creator_id: int,
    payload: CreatorUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_authenticated),
):
    """
    Update creator.
    Owner or admin only.
    """

    creator = update_creator_service(
        db=db,
        creator_id=creator_id,
        payload=payload,
        current_user=current_user,
    )

    return CreatorDTO.model_validate(
        creator
    )


# =========================================================
# DELETE CREATOR
# =========================================================

@router.delete(
    "/{creator_id}",
    response_model=APIResponse,
)
def delete_creator(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user : User = Depends(require_authenticated),
):
    """
    Delete creator.
    Owner or admin only.
    """

    delete_creator_service(
        db=db,
        creator_id=creator_id,
        current_user=current_user,
    )

    return APIResponse(
        message= "Creator deleted successfully",
        data=None,
    )


# =========================================================
# GET CREATOR PRICING
# =========================================================

@router.get(
    "/{creator_id}/pricing",
    response_model=APIResponse,
)
def get_creator_pricing(
    creator_id: int,
    db: Session = Depends(get_db),
    current_user : User = Depends(require_authenticated),
):
    """
    Fetch creator pricing.
    Owner or admin only.
    """

    if creator_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid creator ID",
        )

    creator = get_creator_by_id_service(
        db,
        creator_id,
    )

    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found",
        )

    if (
        creator.user_id != current_user.id
        and not current_user.is_admin
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to access this creator",
        )

    result = get_creator_pricing_service(
        db=db,
        creator_id=creator_id,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pricing data not found",
        )

    return APIResponse(
        message="Pricing fetched successfully",
        data=result,
    )