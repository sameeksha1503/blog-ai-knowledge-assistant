from typing import Annotated,List
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select,Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from .model import Post
from .schemas import PostCreate,PostUpdate,PostRead
from ..comments.schemas import CommentRead
from ..agent.tools import vector_store
from ..database import get_db
from ..auth import get_current_user

router=APIRouter(prefix="/posts",tags=["Posts"])

#--------------------------------------------------------------------------------------------------------

@router.get('/', response_model=List[PostRead])
async def read_posts(
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):

    posts= (await db.exec(select(Post))).all()
    return posts

#-------------------------------------------------------------------------------------------------------------

@router.post('/',response_model=PostRead)
async def create_post(
    post:PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):

    new_post=Post(**post.model_dump(),author_id=current_user_id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    await vector_store.aadd_texts(
        texts=[f"Title: {new_post.title}\nContent: {new_post.content}"],
        metadatas=[{
            "post_id": new_post.id,
            "user_id": current_user_id,
            "content_type": "post"
        }]
    )

    return new_post

#-----------------------------------------------------------------------------------------------------------------

@router.get('/{post_id}',response_model=PostRead)
async def read_post(
    post_id:int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    
    post= await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return post
#----------------------------------------------------------------------------------------------------------------------

@router.patch('/{post_id}')
async def update_post(
    post_id:int,
    updated_post: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query=select(Post).where(Post.id == post_id,Post.author_id == current_user_id) 
    post = (await db.exec(query)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found or unauthorised access")
        
    updated_data = updated_post.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(post, key, value)

    db.add(post)
    await db.commit()
    await db.refresh(post)

    await vector_store.adelete(filter={"post_id":post_id,"content_type":"post"})

    await vector_store.aadd_texts(
        texts=[f"Title: {post.title}\nContent: {post.content}"],
        metadatas=[{
            "post_id":post.id,
            "user_id":current_user_id,
            "content_type":"post"
        }]
    )
    return post
#-----------------------------------------------------------------------------------------------------------------------------

@router.delete('/{post_id}')
async def delete_post(
    post_id:int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query=select(Post).where(Post.id == post_id,Post.author_id == current_user_id)
    post = (await db.exec(query)).one_or_none()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found or unauthorised access")
            
    await db.delete(post)
    await db.commit()

    await vector_store.adelete(filter={"post_id":post_id})

    return {"message":"Post successfully deleted"}

#-------------------------------------------------------------------------------------------------------------------------------------
@router.get('/{post_id}/comments', response_model=List[CommentRead])
async def read_post_comment(
    post_id:int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query= select(Post).options(selectinload(Post.comments)).where(Post.id == post_id)
    post=(await db.exec(query)).first()
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")

    return post.comments