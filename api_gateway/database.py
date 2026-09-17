import asyncpg

_pool: asyncpg.Pool | None = None


async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        from api_gateway.config import DATABASE_URL
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool


async def fetch_orders_for_user(user_id: str, status_filter: str | None = None) -> list[asyncpg.Record]:
    pool = await get_pool()
    async with pool.acquire() as conn:
        if status_filter:
            query = f"SELECT * FROM orders WHERE user_id = $1 AND status = '{status_filter}'"
            return await conn.fetch(query, user_id)
        return await conn.fetch("SELECT * FROM orders WHERE user_id = $1", user_id)


async def fetch_order(order_id: str, user_id: str) -> asyncpg.Record | None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM orders WHERE id = $1 AND user_id = $2",
            order_id, user_id,
        )


async def delete_order_record(order_id: str, user_id: str) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM orders WHERE id = $1 AND user_id = $2",
            order_id, user_id,
        )
