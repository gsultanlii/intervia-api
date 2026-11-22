from fastapi import Header

from app.mock_data import USERS
from app.responses import ApiError


def get_current_user(authorization: str | None = Header(default=None)):
    """Return the user for the Bearer token, or raise 401."""
    if authorization is None:
        raise ApiError(401, "UNAUTHORIZED", "Authentication token is missing.")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise ApiError(401, "UNAUTHORIZED", "Authorization header must be 'Bearer <token>'.")

    user = USERS.get(parts[1])
    if user is None:
        raise ApiError(401, "UNAUTHORIZED", "Authentication token is invalid.")

    return user
