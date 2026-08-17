from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text  
from .db.database import engine, Base
from .routers import auth, repository

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # 1. Execute the command to enable pgvector on the database
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        
        # 2. FORCE DROP THE OLD TABLES (COMMENT THESE OUT!)
        # await conn.execute(text('DROP TABLE IF EXISTS "Chunks" CASCADE;'))
        # await conn.execute(text('DROP TABLE IF EXISTS "Repositories" CASCADE;'))
        
        # Now safely wipe anything else SQLAlchemy knows about (COMMENT THIS OUT!)
        # await conn.run_sync(Base.metadata.drop_all)
        # print("🗑️ All old tables dropped successfully.")
        
        # 3. Create tables using the brand new Parent-Child models (LEAVE THIS)
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tables verified/created successfully.")

        # 4. Build the HNSW Index (LEAVE THIS)
        hnsw_query = text("""
            CREATE INDEX IF NOT EXISTS file_chunks_hnsw_idx 
            ON file_chunks USING hnsw (chunk_embedding vector_cosine_ops) 
            WITH (m = 16, ef_construction = 64);
        """)
        await conn.execute(hnsw_query)
        print("✅ HNSW Vector Index is ready.")
        
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(repository.router)