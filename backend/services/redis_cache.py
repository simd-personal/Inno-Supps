"""
Redis cache service for Inno Supps
"""

import json
import redis
from typing import Any, Optional, List, Dict
from datetime import datetime, timedelta
from backend.config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL in seconds"""
        try:
            serialized_value = json.dumps(value, default=str)
            if ttl:
                return self.redis_client.setex(key, ttl, serialized_value)
            else:
                return self.redis_client.set(key, serialized_value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def mget(self, keys: List[str]) -> List[Optional[Any]]:
        """Get multiple values from cache"""
        try:
            values = self.redis_client.mget(keys)
            result = []
            for value in values:
                if value:
                    result.append(json.loads(value))
                else:
                    result.append(None)
            return result
        except Exception as e:
            print(f"Redis mget error: {e}")
            return [None] * len(keys)
    
    def mset(self, mapping: Dict[str, Any]) -> bool:
        """Set multiple values in cache"""
        try:
            serialized_mapping = {
                key: json.dumps(value, default=str) 
                for key, value in mapping.items()
            }
            return self.redis_client.mset(serialized_mapping)
        except Exception as e:
            print(f"Redis mset error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False
    
    def ttl(self, key: str) -> int:
        """Get TTL for key in seconds"""
        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            print(f"Redis ttl error: {e}")
            return -1
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment key by amount"""
        try:
            return self.redis_client.incrby(key, amount)
        except Exception as e:
            print(f"Redis incr error: {e}")
            return None
    
    def expire(self, key: str, ttl: int) -> bool:
        """Set TTL for existing key"""
        try:
            return bool(self.redis_client.expire(key, ttl))
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False
    
    def flushdb(self) -> bool:
        """Flush current database (use with caution)"""
        try:
            return self.redis_client.flushdb()
        except Exception as e:
            print(f"Redis flushdb error: {e}")
            return False

# Global cache instance
cache = RedisCache()
