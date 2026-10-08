from typing import Annotated
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select,Session
from sqlmodel.ext.asyncio.session import AsyncSession

from .model import Comment
from .schemas import CommentCreate, CommentRead
from ..database import get_db
from ..auth import get_current_user
from ..agent.tools import vector_store

router=APIRouter(prefix="/comments",tags=["Comments"])

#-------------------------------------------------------------------------------------------------------
@router.post('/',response_model=CommentRead)
async def create_comment(
    comment:CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    new_comment=Comment(**comment.model_dump(),user_id=current_user_id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    await vector_store.aadd_texts(
        texts=[new_comment.content],
        metadatas=[{
            "comment_id":new_comment.id,
            "post_id":new_comment.post_id,
            "user_id":current_user_id,
            "content_type":"comment"
        }]
    )
    return new_comment

#-----------------------------------------------------------------------------------------------------------------
@router.get('/{comment_id}',response_model=CommentRead)
async def read_comment(
    comment_id:int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):

    comment=await db.get(Comment,comment_id)
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    return comment

#--------------------------------------------------------------------------------------------------------------------
@router.delete('/{comment_id}')
async def delete_comment(comment_id:int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query=select(Comment).where(Comment.id == comment_id,Comment.user_id == current_user_id)
    comment = (await db.exec(query)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found or unauthorised access")
   
    await db.delete(comment)
    await db.commit()

    await vector_store.adelete(filter={"comment_id":comment_id})
    
    return {"message":"Comment successfully deleted"}









