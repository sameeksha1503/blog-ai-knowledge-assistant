from pydantic import BaseModel

#-------------- User Schemas-------------
class UserCreate(BaseModel):
    username:str
    password:str

# class UserLogin(BaseModel):
#     username:str
#     password:str




