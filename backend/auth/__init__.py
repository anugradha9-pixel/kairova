"""
Kairova Auth Module

Clean public interface for authentication system.
This module exposes ONLY stable APIs for the rest of the backend.
"""

# =====================================
# SCHEMAS (PUBLIC DTOs)
# =====================================

from backend.auth.schemas import (
    UserSignup,
    UserLogin,
    TokenPair,
    RefreshRequest,
    LogoutRequest,
    UserResponse,
    MessageResponse,
)

# =====================================
# CORE SERVICES (PUBLIC API ONLY)
# =====================================

from backend.auth.service import (
    create_user,
    login_user,
    refresh_user_tokens,
    logout_user,
)

# =====================================
# DEPENDENCIES (FASTAPI INJECTION LAYER)
# =====================================

from backend.auth.dependencies import (
    get_current_user,
    get_token_payload,
)

# =====================================
# PUBLIC EXPORT CONTRACT
# =====================================

__all__ = [
    # schemas
    "UserSignup",
    "UserLogin",
    "TokenPair",
    "RefreshRequest",
    "LogoutRequest",
    "UserResponse",
    "MessageResponse",

    # services
    "create_user",
    "login_user",
    "refresh_user_tokens",
    "logout_user",

    # dependencies
    "get_current_user",
    "get_token_payload",
]