from fastapi import APIRouter, Depends, HTTPException, status
from ..core.security import get_current_user 
from ..db.database import get_db
from sqlalchemy.orm import session
from ..db import models
from ..schemas import repository
from .support_functions import read_repository, chunk_repository, embedding_chunks

import subprocess
from pathlib import Path

router = APIRouter()

@router.post("/repository_analysis")
def get_repository(repository_url:repository.RequestURL, db:session=Depends(get_db), current_user=Depends(get_current_user)):

    github_url = repository_url.url.rstrip("/")

    if not github_url.startswith("https://github.com/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid GitHub repository URL")

    url_parts = github_url.split("/")

    if len(url_parts) != 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid Github repository URL")

    repo_owner, repo_name = url_parts[-2], url_parts[-1]

    BASE_DIR = Path("repositories")
    BASE_DIR.mkdir(exist_ok=True)

    destination = BASE_DIR/repo_name

    try:
        subprocess.run([
            "git",
            "clone",
            github_url,
            destination
        ],
        check=True
        )

    except subprocess.CalledProcessError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to clone github repository")


    # save to database 

    new_repository = models.Repository(
        user_id = current_user.id,
        repo_url = repository_url.url,    
        repo_name = repo_name,
        repo_owner = repo_owner  
    )

    db.add(new_repository)
    db.commit()
    db.refresh(new_repository)

    # read repository files 

    repository_files = read_repository(destination)

    repository_chunks = chunk_repository(repository_files, 1000, 200, repo_name, repo_owner)

    embedded_chunks = embedding_chunks(repository_chunks)


    for chunk in embedded_chunks:
        new_chunk = models.Chunk(
            repository_id = new_repository.id,
            chunk_index = chunk["chunk_index"],
            chunk_text = chunk["chunk_text"],
            chunk_embedding = chunk["embedding"],
            chunk_metadata = [{
                "chunk_file_path" : chunk["file_path"],
                "chunk_name" : chunk["Repo_name"],
                "chunk_owner" : chunk["Repo_owner"],
                "chunk_index" : chunk["chunk_index"],
            }]
        )

        db.add(new_chunk)
    db.commit()

    return{"Repository_id" : new_repository.id,
           "chunk_embedding" : len(embedded_chuns)}