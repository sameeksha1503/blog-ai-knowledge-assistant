from typing import Annotated
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select,Session

from .model import Comment
from ..comments.schemas import CommentCreate
from ..database import get_session
from ..auth import get_current_user

router=APIRouter(prefix="/comments",tags=["Comments"])
SessionDep=Depends(get_session)
CURRENT_USER=Depends(get_current_user)

@router.post('/')
def create_comment(comment:CommentCreate,session:Annotated[Session, SessionDep],current_user:str=CURRENT_USER):
    new_comment=Comment(**comment.dict(),user_id=current_user)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.get('/{comment_id}')
def read_comment(comment_id:int,session:Annotated[Session, SessionDep],current_user:str=CURRENT_USER):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    return comment

@router.delete('/{comment_id}')
def delete_comment(comment_id:int,session:Annotated[Session, SessionDep],current_user:str=CURRENT_USER):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    if comment.user_id!=current_user:
        raise HTTPException(status_code=403,details="Not authorized to delete this comment")
    session.delete(comment)
    session.commit()
    return {"message":"Comment successfully deleted"}