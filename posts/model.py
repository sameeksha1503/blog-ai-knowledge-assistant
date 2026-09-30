from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime,timezone

from ..users.model import User
from ..comments.model import Comment

class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id:Optional[int]=Field(default=None,primary_key=True)
    title:str
    content:str
    author_id:int=Field(foreign_key="users.id",ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    #Relationships 
    author:Optional[User]=Relationship(back_populates="posts")
    comments:List["Comment"]=Relationship(back_populates="post")

