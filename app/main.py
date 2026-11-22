from fastapi import Depends, FastAPI

from app.auth import get_current_user
from app.interviews import router as interviews_router

app = FastAPI(title="Intervia API", version="1.0.0")
app.include_router(interviews_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/me")
def me(user: dict = Depends(get_current_user)):
    return user