from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import posts,comments

app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
def root():
    print("Root message")
    return {"message":"hello"}