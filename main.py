from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from src.database import create_db_and_tables
from src.users.routers import router as user_router
from src.posts.routers import router as post_router  
from src.comments.routers import router as comment_router
from src.agent.routers import router as agent_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app=FastAPI(title="blog api", lifespan=lifespan)

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(agent_router)

@app.get("/")
async def root():
    print("Root message")
    return {"message":"hello"}