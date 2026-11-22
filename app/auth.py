from fastapi import Header, HTTPException

from app.mock_data import USERS


def get_current_user(authorization: str | None = Header(default=None)):
    """Return the user for the Bearer token, or raise 401."""
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing token.")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header.")

    user = USERS.get(parts[1])
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token.")

    return user
