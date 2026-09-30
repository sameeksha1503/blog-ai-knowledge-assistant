from sqlmodel import SQLModel, Field, Column
from typing import Optional
from datetime import datetime
from pgvector.sqlalchemy import Vector  

class KnowledgeBase(SQLModel, table=True):
    __tablename__ = "knowledge_base"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Track where this chunk came from
    source_type: str = Field(max_length=20)  # 'post' or 'comment'
    source_id: int                            # ID of the post or comment
    post_id: Optional[int] = Field(default=None, foreign_key="post.id", ondelete="CASCADE")

    # Content and chunking metadata
    content: str
    chunk_index: int = Field(default=0)

    # Vector embedding column (1536 dims for OpenAI text-embedding-3-small)
    # Uses Column(Vector(1536)) to integrate pgvector with SQLModel
    embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(1536))
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)