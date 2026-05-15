from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.async_session import get_async_db

from backend.creator.schemas import CreatorCreate

from backend.creator.service import (
    create_creator_service,
    get_creator_pricing_service,
)

from backend.schemas.response import APIResponse

from backend.dto.creator import (
    CreatorDTO,
    CreateCreatorResponse,
)

from backend.dto.mapper import (
    to_pricing_response,
)


router = APIRouter(
    prefix="/creator",
    tags=["Creator"],
)


# =========================================================
# GET CREATOR PRICING
# =========================================================

@router.get("/{creator_id}/pricing")
async def get_creator_pricing_endpoint(
    creator_id: int,
    db: AsyncSession = Depends(get_async_db),
):

    creator, report = await get_creator_pricing_service(
        db,
        creator_id,
    )

    if not creator:
        raise HTTPException(
            status_code=404,
            detail="Creator not found",
        )

    return APIResponse(
        message="Pricing fetched successfully",
        data={
            "creator": CreatorDTO.model_validate(creator),
            "pricing": to_pricing_response(report),
        },
    )


# =========================================================
# CREATE CREATOR
# =========================================================

@router.post("")
async def create_creator_endpoint(
    payload: CreatorCreate,
    db: AsyncSession = Depends(get_async_db),
):

    creator, report = await create_creator_service(
        db,
        payload,
    )

    return APIResponse(
        message="Creator created successfully",
        data=CreateCreatorResponse(
            creator=CreatorDTO.model_validate(creator),
        ),
    )