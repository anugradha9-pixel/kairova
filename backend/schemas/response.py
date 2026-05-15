from pydantic import BaseModel
from typing import Any


class APIResponse(BaseModel):
    success: bool = True
    message: str
    data: Any