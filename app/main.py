from fastapi import Depends, FastAPI

from app.auth import get_current_user
from app.interviews import router as interviews_router
from app.responses import register_error_handlers, success

app = FastAPI(title="Intervia API", version="1.0.0")
register_error_handlers(app)
app.include_router(interviews_router)


@app.get("/health")
def health():
    return success("API is running.", {"status": "ok"})


@app.get("/api/v1/me")
def me(user: dict = Depends(get_current_user)):
    return success("Current user retrieved successfully.", user)