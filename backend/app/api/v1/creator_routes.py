from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.creator.service import (
    create_creator_service,
    get_creator_pricing_service,
)

from app.modules.creator.schemas import (
    CreatorCreate,
    CreatorResponse,
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
):
    """
    Create a creator and generate
    AI-powered pricing intelligence.
    """

    creator = create_creator_service(
        db=db,
        payload=payload,
    )

    if not creator:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create creator",
        )

    return CreatorResponse.model_validate(
        creator,
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
):
    """
    Fetch creator pricing report.
    """

    if creator_id <= 0:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid creator ID",
        )

    result = get_creator_pricing_service(
        db=db,
        creator_id=creator_id,
    )

    # =====================================
    # NOT FOUND
    # =====================================

    if result is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Creator not found",
        )

    # =====================================
    # SUCCESS RESPONSE
    # =====================================

    return APIResponse(
        message="Pricing fetched successfully",
        data=result,
    )