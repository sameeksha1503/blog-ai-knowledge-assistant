from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated

# create an engine
DATABASE_URL="sqlite:///./blog.db"
connect_args={"check_same_thread":False}
engine=create_engine(DATABASE_URL,echo=True,connect_args=connect_args)

# create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create session dependency
def get_session():
    with Session(engine) as session:
        yield session

SessionDep=Annotated[Session,Depends(get_session)]
