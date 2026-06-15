import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from backend.logging.logger import get_logger

logger = get_logger("request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs all incoming HTTP requests with latency.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} "
            f"- status={response.status_code} "
            f"- time={round(process_time * 1000, 2)}ms"
        )

        return response