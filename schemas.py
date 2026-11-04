from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class TokenRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100000)

class OptimizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100000)
    model_name: str = "SampleLLM"

class SessionResponse(BaseModel):
    session_id: str
    started_at: datetime
    expires_at: datetime
    status: Literal["active", "completed"]


class SessionPromptRequest(BaseModel):
    text: str = Field(min_length=1, max_length=100000)
    model_name: str = "SampleLLM"


class SessionStatusResponse(BaseModel):
    session_id: str
    started_at: datetime
    expires_at: datetime
    status: Literal["active", "completed", "expired"]
    remaining_seconds: int