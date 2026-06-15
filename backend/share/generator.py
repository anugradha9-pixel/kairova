import uuid
from typing import Dict, Any


def generate_share_payload(
    creator_id: int,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generates a shareable payload for creator pricing report.
    """

    share_id = str(uuid.uuid4())

    return {
        "share_id": share_id,
        "creator_id": creator_id,
        "data": data,
    }