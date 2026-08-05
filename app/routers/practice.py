from fastapi import APIRouter, Depends, HTTPException, status
from sentence_transformers import SentenceTransformer
from ..db.database import get_db
from sqlalchemy.orm import session
from ..db import models
from ..schemas.repository import Analysis
from typing import List
router = APIRouter()

@router.get("/chat", response_model=List[Analysis])
def report_query(repo_id:int, db:session = Depends(get_db)):

    chunks = db.query(models.Chunk).filter(models.Chunk.repository_id == repo_id).all() 

    return chunks
