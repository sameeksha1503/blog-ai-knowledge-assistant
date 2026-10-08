from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from .schemas import AskRequest
from .agent import agent
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/agent", tags=["Agentic RAG"])

@router.post("/ask")
async def ask_agent(
    request: AskRequest, 
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    user_msg=request.query
    if request.post_id is not None :
        user_msg += f" (Post ID: {request.post_id})"
    try:
        inputs = {
            "messages": [("user", user_msg)],
            "user_id":current_user_id, 
            }
        print(f"Agent inputs: {inputs}")  # Debugging line to check inputs
        result = await agent.ainvoke(inputs)

        response = result["messages"][-1].content

        return {"answer":response}
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )
