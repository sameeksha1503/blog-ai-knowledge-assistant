from typing import Annotated
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from jose import jwt
from datetime import datetime,timedelta,timezone
from sqlalchemy.orm import selectinload

from .model import User
from .schemas import UserCreate
from ..database import get_db


from ..auth import hash_password,verify_password,get_current_user, SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
router=APIRouter(tags=["Users"])



#----------------------------------------------------------------------------------------------

@router.post('/signup')
async def user_signup(
    user:UserCreate,
    db: AsyncSession = Depends(get_db)
    ):

    query= select(User).where(User.username == user.username)
    existing_user= (await db.exec(query)).first()

    if existing_user:
        raise HTTPException(status_code=400,detail="User already exist")
    
    new_user=User(username=user.username,hashed_password=hash_password(user.password))

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

#------------------------------------------------------------------------------------------------------

@router.post('/login')
async def user_login(
    db: AsyncSession = Depends(get_db),
    form_data:OAuth2PasswordRequestForm=Depends()
    ):

    query=select(User).where(User.username==form_data.username)
    user=(await db.exec(query)).first()
    
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid username or password")

    payload={
        "sub":str(user.id),
        "exp":datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":token,"token_type":"bearer" }

#----------------------------------------------------------------------------------------------------------

@router.get('/my_posts')
async def read_user_posts(
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query= select(User).options(selectinload(User.posts)).where(User.id == current_user_id)
    user=(await db.exec(query)).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    return user.posts

#-----------------------------------------------------------------------------------------------------------

@router.get('/comments')
async def read_user_comments(
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
    ):
    query= select(User).options(selectinload(User.comments)).where(User.id == current_user_id)
    user=(await db.exec(query)).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    return user.comments