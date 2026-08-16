from fastapi import APIRouter, Depends, HTTPException, status
from ..core.security import get_current_user 
from ..db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import models
from ..schemas import repository
from ..service import create_repo_chunks, extract_repo_files, generate_chunk_embeddings
from ..service import pgvector_queries, build_report_query, combine_chunks_prompts, report_generation_prompts, prompt_preprocessor
from ..service import llm_service
import subprocess
from pathlib import Path
import asyncio
import tiktoken

router = APIRouter()

@router.post("/repository_analysis")
async def get_repository(repository_url:repository.RequestURL, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):

    github_url = repository_url.url.strip().rstrip("/")

    if not github_url.startswith("https://github.com/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid GitHub repository URL")

    url_parts = github_url.split("/")

    if len(url_parts) != 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please provide a valid Github repository URL")

    repo_owner, repo_name = url_parts[-2], url_parts[-1]

    BASE_DIR = Path("repositories")
    BASE_DIR.mkdir(exist_ok=True)

    # 1. THIS IS THE MAGIC LINE YOU ARE MISSING!
    # It must exist before the print statements.
    destination = BASE_DIR / repo_name

    # 2. Now it is safe to print
    print(f"--> DEBUG URL: '{github_url}'")
    print(f"--> DEBUG DESTINATION: '{destination}'")

    # 3. Now it is safe to check if the folder exists
    if not destination.exists():
        try:
            subprocess.run([
                "git",
                "clone",
                github_url,
                str(destination)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"--> GIT CLONE ERROR: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to clone github repository"
            )
    else:
        print(f"Repository {repo_name} already exists. Skipping clone.")

    # save to database 

    new_repository = models.Repository(
        user_id = current_user.id,
        repo_url = repository_url.url,    
        repo_name = repo_name,
        repo_owner = repo_owner  
    )

    db.add(new_repository)
    await db.commit()
    await db.refresh(new_repository)


    repository_files = extract_repo_files.read_repository(destination)

    repository_chunks = create_repo_chunks.chunk_repository(repository_files, 1000, 200, repo_name, repo_owner)

    chunk_texts = [chunk["chunk_text"] for chunk in repository_chunks]

    chunk_embeddings = generate_chunk_embeddings.embedding_chunks(chunk_texts)

    for chunk, embedding in zip(repository_chunks, chunk_embeddings):
        new_chunk = models.FileChunk(
            repository_id=new_repository.id,
            chunk_index=chunk["chunk_index"],
            chunk_text=chunk["chunk_text"],
            chunk_embedding=embedding,
            chunk_metadata={
                "chunk_file_path": chunk["file_path"],
                "chunk_name": chunk["Repo_name"],
                "chunk_owner": chunk["Repo_owner"],
                "chunk_index": chunk["chunk_index"],
            }
        )

        db.add(new_chunk)

    await db.commit()


    # report queries

    summary_query = pgvector_queries.REPOSITORY_SUMMARY_QUERY
    technology_stack_query = pgvector_queries.TECHNOLOGY_STACK_QUERY
    architecture_flow_query = pgvector_queries.ARCHITECTURE_FLOW_QUERY
    architecture_review_query = pgvector_queries.ARCHITECTURE_REVIEW_QUERY
    database_flow_query = pgvector_queries.DATABASE_FLOW_QUERY
    database_review_query = pgvector_queries.DATABASE_REVIEW_QUERY
    security_review_query = pgvector_queries.SECURITY_REVIEW_QUERY
    production_review_query = pgvector_queries.PRODUCTION_REVIEW_QUERY 
    documentation_review_query = pgvector_queries.DOCUMENTATION_REVIEW_QUERY
    code_quality_review_query = pgvector_queries.CODE_QUALITY_REVIEW_QUERY
    contributions_query = pgvector_queries.CONTRIBUTION_QUERY  

    queries = []

    queries.extend([
        summary_query,
        technology_stack_query,
        architecture_flow_query,
        architecture_review_query,
        database_flow_query,
        database_review_query,
        security_review_query,
        production_review_query,
        documentation_review_query,
        code_quality_review_query,
        contributions_query
    ])

    reports_queries = generate_chunk_embeddings.embedding_chunks(queries)


    # Retrieve relevant chunks 

    repo_id = new_repository.id


    (
        repository_summary_relevant_chunks,
        technology_stack_relevant_chunks,
        architecture_flow_relevant_chunks,
        database_flow_relevant_chunks,
        architecture_review_relevant_chunks,
        code_quality_review_relevant_chunks,
        security_review_relevant_chunks,
        production_review_relevant_chunks,
        database_review_relevant_chunks,
        documentation_review_relevant_chunks,
        contribution_relevant_chunks,
    ) = await asyncio.gather(
        build_report_query.report_query(
            repo_id,
            reports_queries[0],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[1],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[2],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[4],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[3],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[9],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[6],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[7],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[5],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[8],
            db
        ),
        build_report_query.report_query(
            repo_id,
            reports_queries[10],
            db
        ),
    )

    # combine identical report chunks

    summary_technology_stack_relevant_chunks = combine_chunks_prompts.combine_retrieval_chunks(repository_summary_relevant_chunks , technology_stack_relevant_chunks)

    architecture_flow_database_flow_relevant_chunks = combine_chunks_prompts.combine_retrieval_chunks(architecture_flow_relevant_chunks , database_flow_relevant_chunks)

    architecture_review_code_quality_review_relevant_chunks = combine_chunks_prompts.combine_retrieval_chunks(architecture_review_relevant_chunks, code_quality_review_relevant_chunks)

    production_review_security_review_relevant_chunks = combine_chunks_prompts.combine_retrieval_chunks(production_review_relevant_chunks, security_review_relevant_chunks)


    # combine identical report prompts

    summary_technology_stack_prompt = combine_chunks_prompts.summary_technology_stack_prompts(report_generation_prompts.REPOSITORY_SUMMARY_PROMPT, report_generation_prompts.TECHNOLOGY_STACK_PROMPT)

    architecture_flow_database_flow_prompt = combine_chunks_prompts.architecture_flow_database_flow_prompts(report_generation_prompts.ARCHITECTURE_FLOW_PROMPT, report_generation_prompts.DATABASE_FLOW_PROMPT)

    architecture_review_code_quality_review_prompt = combine_chunks_prompts.architecture_review_code_quality_review_prompts(report_generation_prompts.ARCHITECTURE_REVIEW_PROMPT, report_generation_prompts.CODE_QUALITY_PROMPT)

    production_review_security_review_prompt = combine_chunks_prompts.production_review_security_review_prompts(report_generation_prompts.PRODUCTION_READINESS_PROMPT, report_generation_prompts.SECURITY_REVIEW_PROMPT)

    database_review_prompt = report_generation_prompts.DATABASE_REVIEW_PROMPT

    documentation_review_prompt = report_generation_prompts.DOCUMENTATION_REVIEW_PROMPT

    contributions_analysis_prompt = report_generation_prompts.CONTRIBUTIONS_PROMPT


    # final llm prompt 

    summary_technology_stack_llm_prompt = prompt_preprocessor.final_prompt(summary_technology_stack_relevant_chunks, summary_technology_stack_prompt)

    architecture_flow_database_flow_llm_prompt = prompt_preprocessor.final_prompt(architecture_flow_database_flow_relevant_chunks, architecture_flow_database_flow_prompt)

    architecture_review_code_quality_review_llm_prompt = prompt_preprocessor.final_prompt(architecture_review_code_quality_review_relevant_chunks, architecture_review_code_quality_review_prompt)

    production_review_security_review_llm_prompt = prompt_preprocessor.final_prompt(production_review_security_review_relevant_chunks, production_review_security_review_prompt)

    database_review_llm_prompt = prompt_preprocessor.final_prompt(database_review_relevant_chunks, database_review_prompt)

    documentation_review_llm_prompt = prompt_preprocessor.final_prompt(documentation_review_relevant_chunks, documentation_review_prompt)

    contributions_analysis_llm_prompt = prompt_preprocessor.final_prompt(contribution_relevant_chunks, contributions_analysis_prompt)

    # Measuring token size

    encoding = tiktoken.get_encoding("cl100k_base")

    for name, prompt in [
        ("summary_technology_stack", summary_technology_stack_llm_prompt),
        ("architecture_flow_database_flow", architecture_flow_database_flow_llm_prompt),
        ("architecture_review_code_quality", architecture_review_code_quality_review_llm_prompt),
        ("production_security", production_review_security_review_llm_prompt),
        ("database_review", database_review_llm_prompt),
        ("documentation_review", documentation_review_llm_prompt),
        ("contributions", contributions_analysis_llm_prompt),
    ]:
        tokens = len(encoding.encode(prompt))
        print(f"{name}: {tokens} tokens")

        
    #llm_report_generation

    print("Executing all 7 LLM requests concurrently via Cohere...")
    
    (
        summary_technology_stack,
        architecture_flow_database_flow,
        architecture_review_code_quality_review,
        production_review_security_review,
        database_review,
        documentation_review,
        contributions_analysis,
    ) = await asyncio.gather(
        llm_service.final_report(summary_technology_stack_llm_prompt),
        llm_service.final_report(architecture_flow_database_flow_llm_prompt),
        llm_service.final_report(architecture_review_code_quality_review_llm_prompt),
        llm_service.final_report(production_review_security_review_llm_prompt),
        llm_service.final_report(database_review_llm_prompt),
        llm_service.final_report(documentation_review_llm_prompt),
        llm_service.final_report(contributions_analysis_llm_prompt),
    ) 

    print("All 7 reports generated successfully!")

    # Unpack the dictionaries to separate the keys
    
    return {
        # Unpacking Project Overview
        "repository_summary": summary_technology_stack.get("repository_summary", {}),
        "technology_stack": summary_technology_stack.get("technology_stack", {}),
        
        # Unpacking Architecture & Database Flow
        "architecture_flow": architecture_flow_database_flow.get("architecture_flow", {}),
        "database_flow": architecture_flow_database_flow.get("database_flow", {}),
        
        # Unpacking Architecture & Code Quality Review
        "architecture_review": architecture_review_code_quality_review.get("architecture_review", {}),
        "code_quality_review": architecture_review_code_quality_review.get("code_quality_review", {}),
        
        # Unpacking Production & Security Review
        "production_review": production_review_security_review.get("production_review", {}),
        "security_review": production_review_security_review.get("security_review", {}),
        
        # These are already standalone
        "database_review": database_review,
        "documentation_review": documentation_review,
        "contributions_analysis": contributions_analysis,
    }