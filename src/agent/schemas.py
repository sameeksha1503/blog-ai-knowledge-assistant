from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class AskRequest(BaseModel):
    query: str = Field(..., example="Summarize what people are saying here")
    post_id: int | None = Field(None, description="query related to 'post'")