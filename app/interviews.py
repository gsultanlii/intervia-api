from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.auth import get_current_user
from app.mock_data import INTERVIEWS
from app.schemas import Interview, InterviewCreate, InterviewUpdate

router = APIRouter(prefix="/api/v1/interviews", tags=["interviews"])


def _is_admin(user: dict) -> bool:
    return user["role"] == "admin"


def _get_interview_or_404(interview_id: str, user: dict) -> dict:
    """Return the interview if it exists and the user may access it.

    Not-owner and not-found both give 404, so we do not reveal
    that someone else's interview exists.
    """
    interview = INTERVIEWS.get(interview_id)
    if interview is None or (
        interview["ownerId"] != user["id"] and not _is_admin(user)
    ):
        raise HTTPException(status_code=404, detail="Interview not found.")
    return interview


@router.get("", response_model=list[Interview])
def list_interviews(user: dict = Depends(get_current_user)):
    if _is_admin(user):
        return list(INTERVIEWS.values())
    return [i for i in INTERVIEWS.values() if i["ownerId"] == user["id"]]


@router.get("/{interview_id}", response_model=Interview)
def get_interview(interview_id: str, user: dict = Depends(get_current_user)):
    return _get_interview_or_404(interview_id, user)


@router.post("", response_model=Interview, status_code=status.HTTP_201_CREATED)
def create_interview(
    body: InterviewCreate,
    response: Response,
    user: dict = Depends(get_current_user),
):
    interview_id = f"interview_{uuid4().hex[:8]}"
    interview = {
        "id": interview_id,
        "ownerId": user["id"],
        "jobTitle": body.jobTitle,
        "jobDescription": body.jobDescription,
        "mode": body.mode,
        "status": "ready",
        "score": None,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    INTERVIEWS[interview_id] = interview
    response.headers["Location"] = f"/api/v1/interviews/{interview_id}"
    return interview


@router.put("/{interview_id}", response_model=Interview)
def update_interview(
    interview_id: str,
    body: InterviewUpdate,
    user: dict = Depends(get_current_user),
):
    interview = _get_interview_or_404(interview_id, user)
    interview.update(body.model_dump())
    return interview


@router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interview(interview_id: str, user: dict = Depends(get_current_user)):
    _get_interview_or_404(interview_id, user)
    del INTERVIEWS[interview_id]