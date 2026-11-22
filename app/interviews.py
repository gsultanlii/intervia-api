from datetime import datetime, timezone
from itertools import count
from typing import Literal, Optional

from fastapi import APIRouter, Depends, Query, Response

from app.auth import get_current_user
from app.mock_data import INTERVIEWS
from app.responses import ApiError, success
from app.schemas import InterviewCreate, InterviewUpdate

router = APIRouter(prefix="/api/v1/interviews", tags=["interviews"])

_id_counter = count(5)  # interview_1..4 already exist


def _can_access(interview: dict, user: dict) -> bool:
    return user["role"] == "admin" or interview["ownerId"] == user["id"]


def _get_accessible(interview_id: str, user: dict) -> dict:
    """404 for missing AND for other users' interviews (hides existence)."""
    interview = INTERVIEWS.get(interview_id)
    if interview is None or not _can_access(interview, user):
        raise ApiError(404, "NOT_FOUND", "Interview not found.")
    return interview


@router.get("")
def list_interviews(
    page: int = Query(1, ge=1),
    perPage: int = Query(10, ge=1, le=100),
    status: Optional[Literal["ready", "in_progress", "completed"]] = None,
    user: dict = Depends(get_current_user),
):
    items = [i for i in INTERVIEWS.values() if _can_access(i, user)]
    if status:
        items = [i for i in items if i["status"] == status]
    total = len(items)
    start = (page - 1) * perPage
    return success(
        "Interviews retrieved successfully.",
        items[start : start + perPage],
        meta={"total": total, "page": page, "perPage": perPage},
    )


@router.get("/{interview_id}")
def get_interview(interview_id: str, user: dict = Depends(get_current_user)):
    interview = _get_accessible(interview_id, user)
    return success("Interview retrieved successfully.", interview)


@router.post("", status_code=201)
def create_interview(
    body: InterviewCreate, response: Response, user: dict = Depends(get_current_user)
):
    new_id = f"interview_{next(_id_counter)}"
    interview = {
        "id": new_id,
        "ownerId": user["id"],
        "jobTitle": body.jobTitle,
        "jobDescription": body.jobDescription,
        "mode": body.mode,
        "status": "ready",
        "score": None,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    INTERVIEWS[new_id] = interview
    response.headers["Location"] = f"/api/v1/interviews/{new_id}"
    return success("Interview created successfully.", interview)


@router.put("/{interview_id}")
def update_interview(
    interview_id: str, body: InterviewUpdate, user: dict = Depends(get_current_user)
):
    interview = _get_accessible(interview_id, user)
    if interview["status"] == "completed":
        raise ApiError(
            409, "CONFLICT", "A completed interview cannot be modified."
        )
    interview.update(body.model_dump())
    return success("Interview updated successfully.", interview)


@router.delete("/{interview_id}")
def delete_interview(interview_id: str, user: dict = Depends(get_current_user)):
    _get_accessible(interview_id, user)
    del INTERVIEWS[interview_id]
    return success("Interview deleted successfully.", None)