from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__="users"
    id:Optional[int]=Field(default=None,primary_key=True)
    username:str
    hashed_password:str

    posts:List["Post"]=Relationship(back_populates="author")
    comments:List["Comment"]=Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    title:str
    content:str
    author_id:int=Field(foreign_key="users.id")

    author:Optional[User]=Relationship(back_populates="posts")
    comments:List["Comment"]=Relationship(back_populates="post")

class Comment(SQLModel,table=True):
    id:Optional[int]=Field(default=None,primary_key=True)
    content:str
    post_id:int=Field(foreign_key="post.id")
    user_id:int=Field(foreign_key="users.id")

    post:Optional[Post]=Relationship(back_populates="comments")
    user:Optional[User]=Relationship(back_populates="comments")