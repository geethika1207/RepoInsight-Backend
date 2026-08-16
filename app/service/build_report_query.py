from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import models

async def report_query(repo_id: int, embed_query, db: AsyncSession):

    # 1. Fetch the top 10 child chunks
    result = await db.execute(
        select(models.FileChunk)
        .where(models.FileChunk.repository_id == repo_id)
        .order_by(
            models.FileChunk.chunk_embedding.cosine_distance(embed_query) # Fixed typo here!
        )
        .limit(10)
    )

    chunks = result.scalars().all()

    # 2. Extract and deduplicate the Parent IDs
    parent_ids = [chunk.repository_file_id for chunk in chunks]
    parent_ids_without_duplicates = list(set(parent_ids))

    # 3. Fetch ALL parents in a SINGLE query using .in_() works for list only for information retrieval only .. Normally u have to do for loop for retrieving in that case .in
    parent_result = await db.execute(
        select(models.RepositoryFile)
        .where(models.RepositoryFile.id.in_(parent_ids_without_duplicates))
    )

    parents = parent_result.scalars().all()

    # 4. Extract the content from all the fetched parents
    repo_file_content = [parent.file_content for parent in parents]

    return repo_file_content