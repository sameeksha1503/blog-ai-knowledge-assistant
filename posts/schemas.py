from pydantic import BaseModel
from typing import Optional

#-------------- Post Schemas-------------
class PostCreate(BaseModel):
    title:str
    content:str
    # author_id:int

class PostUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None
