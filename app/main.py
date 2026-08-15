from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text  
from .db.database import engine, Base
from .routers import auth, repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    # engine.begin() automatically commits the transaction if there are no errors
    async with engine.begin() as conn:
        # 1. Execute the command to enable pgvector on the database
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        # 2. Create tables (Table MUST exist before we build an index on it)
        await conn.run_sync(Base.metadata.create_all)

        # 3. Build the HNSW Index
        hnsw_query = text("""
            CREATE INDEX IF NOT EXISTS chunks_hnsw_idx 
            ON "Chunks" USING hnsw (chunk_embedding vector_cosine_ops) 
            WITH (m = 16, ef_construction = 64);
        """)
        await conn.execute(hnsw_query)
        print("✅ Tables created and HNSW Vector Index is ready.")
        
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(repository.router)