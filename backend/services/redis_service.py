import redis
import json
import os
from typing import Any, Optional
import asyncio

class RedisService:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from Redis"""
        try:
            return self.redis_client.get(key)
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            return self.redis_client.set(key, value, ex=expire)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter in Redis"""
        try:
            return self.redis_client.incrby(key, amount)
        except Exception as e:
            print(f"Redis increment error: {e}")
            return 0
    
    async def rate_limit_check(self, key: str, limit: int, window: int) -> bool:
        """Check if rate limit is exceeded"""
        try:
            current = await self.increment(key)
            if current == 1:
                self.redis_client.expire(key, window)
            return current <= limit
        except Exception as e:
            print(f"Rate limit check error: {e}")
            return True  # Allow on error
    
    async def cache_embedding(self, text: str, embedding: list) -> bool:
        """Cache embedding result"""
        key = f"embedding:{hash(text)}"
        return await self.set(key, embedding, expire=3600)  # 1 hour
    
    async def get_cached_embedding(self, text: str) -> Optional[list]:
        """Get cached embedding"""
        key = f"embedding:{hash(text)}"
        result = await self.get(key)
        if result:
            return json.loads(result)
        return None
