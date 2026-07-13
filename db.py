import asyncpg
from config import DATABASE_URI

_pool: asyncpg.Pool | None = None

async def get_pool() -> asyncpg.Pool:
    global _pool

    if _pool is None:
        _pool = await asyncpg.create_pool(
            DATABASE_URI,
            min_size=1,
            max_size=10
        )

    return _pool