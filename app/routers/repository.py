from fastapi import APIRouter, Depends, HTTPException, status
from ..core.security import get_current_user 
from ..db.database import get_db
from sqlalchemy.orm import session
from ..db import models
from ..schemas import repository
from .support_functions import read_repository, chunk_repository

import subprocess
from pathlib import Path

router = APIRouter()

@router.post("/repository_analysis")
def get_repository(repository_url:repository.RequestURL, db:session=Depends(get_db)):

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

    # read repository files 

    repository_files = read_repository(destination)

    repository_chunk = chunk_repository(repository_files, 1000, 200, repo_name, repo_owner)

    return repository_chunk