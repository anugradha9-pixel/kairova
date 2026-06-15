import time
from backend.utils.logger import get_logger

logger = get_logger("workers")


def sample_task(creator_id: int):
    """
    Example background task placeholder.
    """

    logger.info(f"Processing creator {creator_id} in background")

    time.sleep(2)

    logger.info(f"Completed processing creator {creator_id}")