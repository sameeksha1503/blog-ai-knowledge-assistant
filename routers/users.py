from fastapi import APIRouter,HTTPException
from sqlmodel import select

from ..models import User
from ..schema import UserCreate,UserLogin
from ..database import SessionDep
from ..auth import hash_password,verify_password

router=APIRouter(tags=["Users"])

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
def user_login(user:UserLogin,session:SessionDep):
    existing_user=session.exec(select(User).where(User.username==user.username)).first()
    if not existing_user or not verify_password(user.password,existing_user.hashed_password):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    return {"message":"Login successfully"}

@router.get('/{user_id}/posts')
def read_post(user_id:int,session:SessionDep):
    user=session.exec(select(User).where(User.id==user_id)).one_or_none()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user.posts