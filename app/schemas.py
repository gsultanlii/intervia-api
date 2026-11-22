from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class InterviewCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    jobTitle: str = Field(min_length=3, max_length=100)
    jobDescription: str = Field(min_length=10, max_length=2000)
    mode: Literal["text", "voice"] = "text"


class InterviewUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    jobTitle: str = Field(min_length=3, max_length=100)
    jobDescription: str = Field(min_length=10, max_length=2000)
    mode: Literal["text", "voice"]
    status: Literal["ready", "in_progress", "completed"]
    score: Optional[int] = Field(default=None, ge=0, le=100)
