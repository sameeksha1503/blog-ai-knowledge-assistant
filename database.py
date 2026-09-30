from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import os

DATABASE_URL = os.getenv( "DATABASE_URL")

# 1. Async Engine
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# create tables
async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# create session dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


