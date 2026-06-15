from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/stripe",
    tags=["Stripe"],
)


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Handles Stripe webhook events.
    """

    payload = await request.json()

    # Placeholder processing logic
    event_type = payload.get("type", "unknown")

    return {
        "status": "received",
        "event": event_type,
    }