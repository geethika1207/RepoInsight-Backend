from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import models


async def report_query(repo_id: int, embed_query: list, db: AsyncSession):

    result = await db.query(
        select(models.Chunk)
        .where(models.Chunk.repository_id == repo_id)
        .order_by(
            models.Chunk.chunk_embedding.cosine_distance(embed_query)
        )
        .limit(16)
    )

    chunks = result.scalars().all()

    return [chunk.chunk_text for chunk in chunks]