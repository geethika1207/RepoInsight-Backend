from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import models

SUPPORTED_EXTENSIONS = {
    ".py", ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".js", ".ts", ".jsx", ".tsx",
    ".java", ".cpp", ".c", ".cs", ".go", ".rs",
    ".php", ".html", ".css", ".sql"
}

# Safe limit for a 128k token context window (roughly 10,000 lines of code)
MAX_TOTAL_CHARACTERS = 350000

async def read_repository(repo_path, db: AsyncSession):
    repository_files = []
    total_character_count = 0

    for file in repo_path.rglob("*"):
        if not file.is_file():
            continue

        if not file.suffix.lower() in SUPPORTED_EXTENSIONS:
            continue

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore" 
            )

            if "\x00" in content:
                continue 
            
            # Check if this file pushes the extraction over the character limit
            total_character_count += len(content)
            if total_character_count > MAX_TOTAL_CHARACTERS:
                raise HTTPException(
                    status_code=413, 
                    detail=f"Repository is too large for the AI context window. The limit is {MAX_TOTAL_CHARACTERS} characters."
                )

            repo_file = models.RepositoryFile(
                file_path=str(file.relative_to(repo_path)),
                file_content=content  
            )

            db.add(repo_file)
            await db.flush() 

            # This sends the actual SQL INSERT command to your PostgreSQL database. Because the database receives the data, it instantly generates the primary key (id) for that row. However, the save is not permanent yet. It is sitting in a pending transaction.

            # 3. Access the ID using dot notation on the SQLAlchemy object
            repository_files.append({
                "file_path": repo_file.file_path,
                "content": content,
                "repo_files_id": repo_file.id 
            })

        except HTTPException:
            raise
        except Exception:
            continue

    # 4. Commiting the entire batch in ONE transaction at the very end
    await db.commit()

    # This tells PostgreSQL to permanently save all the flushed transactions to the hard drive.

    return repository_files