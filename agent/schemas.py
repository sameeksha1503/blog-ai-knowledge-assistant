from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AskRequest(BaseModel):
    query: str = Field(
        ..., 
        min_length=3,
        description="The user query or analytical question for the AI Agent.",
        example="Which post received the most negative feedback?"
    )

class AskResponse(BaseModel):
    query: str = Field(..., description="The query submitted by the user.")
    answer: str = Field(..., description="The agent's response.")
    
class AgentErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message if agent execution fails.")