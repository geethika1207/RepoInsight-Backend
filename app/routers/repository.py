from fastapi import APIRouter, Depends, HTTPException, status
from ..core.security import get_current_user 
from ..db.database import get_db
from sqlalchemy.orm import session
from ..db import models
from ..schemas import repository
from ..service import create_repo_chunks, extract_repo_files, generate_chunk_embeddings
from ..service import prompt_templates, build_report_query
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


    repository_files = extract_repo_files.read_repository(destination)

    repository_chunks = create_repo_chunks.chunk_repository(repository_files, 1000, 200, repo_name, repo_owner)

    embedded_chunks = generate_chunk_embeddings.embedding_chunks(repository_chunks)


    for chunk in embedded_chunks:
        new_chunk = models.Chunk(
            repository_id = new_repository.id,
            chunk_index = chunk["chunk_index"],
            chunk_text = chunk["chunk_text"],
            chunk_embedding = chunk["embedding"],
            chunk_metadata = {
                "chunk_file_path" : chunk["file_path"],
                "chunk_name" : chunk["Repo_name"],
                "chunk_owner" : chunk["Repo_owner"],
                "chunk_index" : chunk["chunk_index"],
            }
        )

        db.add(new_chunk)
    db.commit()

    repo_id = new_repository.id

    repository_summary_relevant_chunks = build_report_query.report_query(
    repo_id,
    prompt_templates.REPOSITORY_SUMMARY_QUERY,
    db
    )

    technology_stack_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.TECHNOLOGY_STACK_QUERY,
        db
    )

    architecture_flow_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.ARCHITECTURE_FLOW_QUERY,
        db
    )

    architecture_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.ARCHITECTURE_REVIEW_QUERY,
        db
    )

    database_flow_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.DATABASE_FLOW_QUERY,
        db
    )

    database_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.DATABASE_REVIEW_QUERY,
        db
    )

    api_flow_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.API_FLOW_QUERY,
        db
    )

    api_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.API_REVIEW_QUERY,
        db
    )

    security_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.SECURITY_REVIEW_QUERY,
        db
    )

    production_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.PRODUCTION_REVIEW_QUERY,
        db
    )

    documentation_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.DOCUMENTATION_REVIEW_QUERY,
        db
    )

    code_quality_review_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.CODE_QUALITY_REVIEW_QUERY,
        db
    )

    improvement_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.IMPROVEMENT_QUERY,
        db
    )

    contribution_relevant_chunks = build_report_query.report_query(
        repo_id,
        prompt_templates.CONTRIBUTION_QUERY,
        db
    )


    return contribution_relevant_chunks