from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text  # 1. Import text from sqlalchemy
from .db.database import engine, Base
from .routers import auth, repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # 2. Execute the command to enable pgvector on the database
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        # 3. Create tables
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(repository.router)