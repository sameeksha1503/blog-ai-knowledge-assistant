from fastapi import APIRouter,HTTPException
from sqlmodel import select

from ..models import Post
from ..schema import PostCreate
from ..database import SessionDep

router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get('/')
def read_posts(session:SessionDep):
    return session.exec(select(Post)).all()

@router.post('/')
def create_post(post:PostCreate,session:SessionDep):
    new_post=Post(**post.dict())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@router.get('/{post_id}')
def read_post(post_id:int,session:SessionDep):
    post=session.exec(select(Post).where(Post.id==post_id)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return post

@router.delete('/{post_id}')
def delete_post(post_id:int,session:SessionDep):
    post=session.exec(select(Post).where(Post.id==post_id)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    session.delete(post)
    session.commit()
    return {"message":"Post successfully deleted"}

@router.get('/{post_id}/comments')
def read_post(post_id:int,session:SessionDep):
    post=session.exec(select(Post).where(Post.id==post_id)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return post.comments