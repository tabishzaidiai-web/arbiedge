"""Redis connection manager with caching helpers."""

import json
from typing import Any, Optional
import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()

redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL,
    decode_responses=True,
    max_connections=20,
)


async def get_redis() -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)


async def get_cached(key: str) -> Optional[Any]:
    r = redis.Redis(connection_pool=redis_pool)
    data = await r.get(key)
    if data:
        return json.loads(data)
    return None


async def set_cached(key: str, value: Any, ttl: int = 3600) -> None:
    r = redis.Redis(connection_pool=redis_pool)
    await r.set(key, json.dumps(value, default=str), ex=ttl)


async def invalidate_cache(pattern: str) -> None:
    r = redis.Redis(connection_pool=redis_pool)
    keys = []
    async for key in r.scan_iter(match=pattern):
        keys.append(key)
    if keys:
        await r.delete(*keys)
