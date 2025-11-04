from pydantic import BaseModel
from typing import Optional

#-------------- Post Schemas-------------
class PostCreate(BaseModel):
    title:str
    content:str

#-------------- Comment Schemas-------------
class CommentCreate(BaseModel):
    content:str
    post_id:int

