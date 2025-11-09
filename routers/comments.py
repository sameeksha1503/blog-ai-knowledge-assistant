from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select

from ..models import Comment
from ..schema import CommentCreate
from ..database import SessionDep
from ..auth import get_current_user

router=APIRouter(prefix="/comments",tags=["Comments"])

@router.post('/')
def create_comment(comment:CommentCreate,session:SessionDep,current_user:str=Depends(get_current_user)):
    new_comment=Comment(**comment.dict(),user_id=current_user)
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.get('/{comment_id}')
def read_comment(comment_id:int,session:SessionDep,current_user:str=Depends(get_current_user)):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    return comment

@router.delete('/{comment_id}')
def delete_comment(comment_id:int,session:SessionDep,current_user:str=Depends(get_current_user)):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    if comment.user_id!=current_user:
        raise HTTPException(status_code=403,details="Not authorized to delete this comment")
    session.delete(comment)
    session.commit()
    return {"message":"Comment successfully deleted"}