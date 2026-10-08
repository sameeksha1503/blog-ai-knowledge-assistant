from sqlmodel import SQLModel, Field, Relationship,DateTime
from typing import Optional
from datetime import datetime,timezone

# from ..users.model import User
# from ..posts.model import Post

class Comment(SQLModel,table=True):
    __tablename__ = "comments"

    id:int|None=Field(default=None,primary_key=True)
    content:str
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
        )

    post:Optional["Post"]=Relationship(back_populates="comments")
    user:Optional["User"]=Relationship(back_populates="comments")