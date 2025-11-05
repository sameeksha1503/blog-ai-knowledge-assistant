from fastapi import APIRouter,HTTPException
from sqlmodel import select

from ..models import Post
from ..schema import PostCreate,PostUpdate
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

@router.put('/{post_id}')
def update_post(post_id:int,updated_post:PostUpdate,session:SessionDep):
    post=session.exec(select(Post).where(Post.id==post_id)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    if updated_post.title is not None:
        post.title=updated_post.title
    if updated_post.content is not None:
        post.content=updated_post.content
    session.add(post)
    session.commit()
    session.refresh(post)
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