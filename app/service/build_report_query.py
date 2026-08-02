from sentence_transformers import SentenceTransformer
from ..db.database import get_db
from sqlalchemy.orm import session
from ..db import models
model = SentenceTransformer("all-MiniLM-L6-v2")

def report_query(repo_id:int, query:str, db:session):

    embed_query = model.encode(query).tolist()

    chunks = (
        db.query(models.Chunk)
        .filter(models.Chunk.repository_id == repo_id)
        .order_by(
            models.Chunk.chunk_embedding.cosine_distance(embed_query)
        )
        .limit(16)
        .all()
    )

    return chunks 
