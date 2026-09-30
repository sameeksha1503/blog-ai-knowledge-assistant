from pydantic import BaseModel

#-------------- Comment Schemas-------------
class CommentCreate(BaseModel):
    content:str
    post_id:int
    # user_id:int