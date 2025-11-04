from fastapi import APIRouter,HTTPException
from sqlmodel import select

from ..models import Comment
from ..schema import CommentCreate
from ..database import SessionDep

router=APIRouter(prefix="/comments",tags=["Comments"])

@router.get('/')
def read_comments(session:SessionDep):
    return session.exec(select(Comment)).all()

@router.post('/')
def create_comment(comment:CommentCreate,session:SessionDep):
    new_comment=Comment(**comment.dict())
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.get('/{comment_id}')
def read_comment(comment_id:int,session:SessionDep):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    return comment

@router.delete('/{comment_id}')
def delete_comment(comment_id:int,session:SessionDep):
    comment=session.exec(select(Comment).where(Comment.id==comment_id)).one_or_none()
    if not comment:
        raise HTTPException(status_code=404,detail="Comment not found")
    session.delete(comment)
    session.commit()
    return {"message":"Comment successfully deleted"}