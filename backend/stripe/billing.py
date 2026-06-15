from typing import Dict, Any


class BillingService:
    """
    Minimal Stripe billing abstraction layer.
    (Placeholder for real Stripe SDK integration)
    """

    def create_checkout_session(
        self,
        creator_id: int,
        amount: float,
    ) -> Dict[str, Any]:
        """
        Simulated checkout session creation.
        Replace with Stripe SDK later.
        """

        return {
            "creator_id": creator_id,
            "amount": amount,
            "status": "checkout_created",
            "checkout_url": f"https://stripe.mock/checkout/{creator_id}",
        }

    def handle_success(self, session_id: str) -> Dict[str, Any]:
        return {
            "session_id": session_id,
            "status": "payment_success",
        }