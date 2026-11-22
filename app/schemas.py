from typing import Literal

from pydantic import BaseModel, Field

InterviewMode = Literal["text", "voice"]
InterviewStatus = Literal["ready", "in_progress", "completed"]


class InterviewCreate(BaseModel):
    """Body for POST /api/v1/interviews."""

    jobTitle: str = Field(min_length=1, max_length=100)
    jobDescription: str = Field(min_length=1, max_length=5000)
    mode: InterviewMode


class InterviewUpdate(BaseModel):
    """Body for PUT /api/v1/interviews/{id} (full replacement)."""

    jobTitle: str = Field(min_length=1, max_length=100)
    jobDescription: str = Field(min_length=1, max_length=5000)
    mode: InterviewMode
    status: InterviewStatus
    score: int | None = Field(default=None, ge=0, le=100)


class Interview(BaseModel):
    """Interview as returned by the API."""

    id: str
    ownerId: str
    jobTitle: str
    jobDescription: str
    mode: InterviewMode
    status: InterviewStatus
    score: int | None
    createdAt: str