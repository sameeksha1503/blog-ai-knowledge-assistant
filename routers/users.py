import datetime
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime,timedelta

from ..models import User
from ..schema import UserCreate
from ..database import SessionDep
from ..auth import hash_password,verify_password,get_current_user

router=APIRouter(tags=["Users"])
SECRET_KEY="your-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

@router.post('/signup')
def user_signup(user:UserCreate,session:SessionDep):
    existing_user=session.exec(select(User).where(User.username==user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exist")
    new_user=User(username=user.username,hashed_password=hash_password(user.password))

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post('/login')
def user_login(session:SessionDep,form_data:OAuth2PasswordRequestForm=Depends()):
    user=session.exec(select(User).where(User.username==form_data.username)).first()
    if not user or not verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    # Create JWT token
    payload={
        "sub":str(user.id),
        "exp":datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token":token,"token_type":"bearer" }

@router.get('/my_posts')
def read_user_posts(session:SessionDep,current_user:str=Depends(get_current_user)):
    user=session.exec(select(User).where(User.id==current_user)).one_or_none()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user.posts

@router.get('/comments')
def read_user_comments(session:SessionDep,current_user:str=Depends(get_current_user)):
    user=session.exec(select(User).where(User.id==current_user)).one_or_none()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user.comments