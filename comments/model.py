from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime,timezone

from ..users.routers import User
from ..posts.routers import Post

class Comment(SQLModel,table=True):
    __tablename__ = "comments"

    id:Optional[int]=Field(default=None,primary_key=True)
    content:str
    post_id: int = Field(foreign_key="post.id", ondelete="CASCADE")
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    #sentiment fields(populated when comment is created)
    sentiment: Optional[str] = Field(default=None, max_length=10) # 'positive', 'negative', 'neutral'
    sentiment_score: Optional[float] = Field(default=None)

    #Relationships
    post:Optional[Post]=Relationship(back_populates="comments")
    user:Optional[User]=Relationship(back_populates="comments")