from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Post(SQLModel, table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    title:str
    content:str
    comments:List["Comment"]=Relationship(back_populates="post")

class Comment(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    content:str
    post_id:int=Field(foreign_key="post.id")
    post:Optional[Post]=Relationship(back_populates="comments")