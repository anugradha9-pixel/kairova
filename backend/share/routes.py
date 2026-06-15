from fastapi import APIRouter

from backend.share.generator import generate_share_payload

router = APIRouter(
    prefix="/share",
    tags=["Share"],
)


@router.post("/{creator_id}")
def create_share_link(creator_id: int, payload: dict):
    """
    Creates a shareable pricing report payload.
    """

    return {
        "message": "Share link generated successfully",
        "data": generate_share_payload(
            creator_id=creator_id,
            data=payload,
        ),
    }