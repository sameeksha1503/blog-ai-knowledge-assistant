from pydantic import BaseModel

#-------------- Post Schemas-------------
class PostCreate(BaseModel):
    title:str
    content:str
    # author_id:int

class PostRead(BaseModel):
    id:int
    title:str
    content:str

class PostUpdate(BaseModel):
    title:str|None=None
    content:str|None=None
