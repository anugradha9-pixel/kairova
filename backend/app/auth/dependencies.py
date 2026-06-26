from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth.repository import AuthRepository
from app.auth.security import verify_access_token
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    payload = verify_access_token(token)

    if not payload:
        raise credentials_exception

    user_id = payload.get("sub")
    session_id = payload.get("sid")

    if not user_id or not session_id:
        raise credentials_exception

    try:
        user_id = int(user_id)

    except (
        TypeError,
        ValueError,
    ):
        raise credentials_exception

    repo = AuthRepository(db)

    session = repo.get_session_by_session_id(
        session_id
    )

    if not session:
        raise credentials_exception

    user = repo.get_user_by_id(
        user_id
    )

    if not user:
        raise credentials_exception

    return user