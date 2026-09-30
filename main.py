from fastapi import FastAPI
from .database import create_db_and_tables
from .posts import routers
from .comments import routers
from .users import routers

app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(routers.router)
app.include_router(routers.router)
app.include_router(routers.router)

@app.get("/")
def root():
    print("Root message")
    return {"message":"hello"}