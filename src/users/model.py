from sqlmodel import SQLModel, Field, Relationship,DateTime
from typing import  List
from datetime import datetime,timezone

# from ..posts.model import Post
# from ..comments.model import Comment

class User(SQLModel, table=True):
    __tablename__="users"

    id:int|None=Field(default=None,primary_key=True)
    username:str
    hashed_password:str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )

    posts:List["Post"]=Relationship(back_populates="author")
    comments:List["Comment"]=Relationship(back_populates="user")


