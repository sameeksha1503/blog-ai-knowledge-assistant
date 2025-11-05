from pydantic import BaseModel
from typing import Optional

#-------------- User Schemas-------------
class UserCreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

#-------------- Post Schemas-------------
class PostCreate(BaseModel):
    title:str
    content:str
    author_id:int

class PostUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None

#-------------- Comment Schemas-------------
class CommentCreate(BaseModel):
    content:str
    post_id:int
    user_id:int

