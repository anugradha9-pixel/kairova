from typing import Any, Optional


class AppException(Exception):
    """
    Base application exception for Kairova backend.
    Supports structured error responses.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: Optional[str] = None,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "app_error"
        self.details = details

        super().__init__(message)


# =========================
# AUTHENTICATION
# =========================

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="authentication_error",
        )


class AuthorizationError(AppException):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="authorization_error",
        )


# =========================
# RESOURCE ERRORS
# =========================

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="not_found",
        )


# =========================
# VALIDATION
# =========================

class ValidationError(AppException):
    def __init__(self, message: str = "Validation error", details: Any = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="validation_error",
            details=details,
        )