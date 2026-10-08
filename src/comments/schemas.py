from pydantic import BaseModel

#-------------- Comment Schemas-------------
class CommentCreate(BaseModel):
    content:str
    post_id:int


class CommentRead(BaseModel):
    id:int
    content:str