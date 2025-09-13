"""
Rate limiter service using Redis token bucket algorithm
"""

import time
from typing import Optional
from backend.services.redis_cache import cache
from backend.config import settings

class RateLimiter:
    def __init__(self):
        self.cache = cache
    
    def is_allowed(self, key: str, limit: int, window_seconds: int) -> bool:
        """
        Check if request is allowed using token bucket algorithm
        
        Args:
            key: Unique identifier for the rate limit (e.g., workspace_id:email)
            limit: Maximum number of requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            True if request is allowed, False otherwise
        """
        current_time = int(time.time())
        bucket_key = f"rate_limit:{key}"
        
        # Get current bucket state
        bucket_data = self.cache.get(bucket_key)
        
        if bucket_data is None:
            # Initialize new bucket
            bucket_data = {
                "tokens": limit - 1,
                "last_refill": current_time
            }
            self.cache.set(bucket_key, bucket_data, window_seconds)
            return True
        
        # Calculate tokens to add based on time passed
        time_passed = current_time - bucket_data["last_refill"]
        tokens_to_add = (time_passed * limit) // window_seconds
        
        if tokens_to_add > 0:
            # Refill tokens
            bucket_data["tokens"] = min(limit, bucket_data["tokens"] + tokens_to_add)
            bucket_data["last_refill"] = current_time
        
        # Check if we have tokens available
        if bucket_data["tokens"] > 0:
            bucket_data["tokens"] -= 1
            self.cache.set(bucket_key, bucket_data, window_seconds)
            return True
        
        return False
    
    def get_remaining_tokens(self, key: str, limit: int, window_seconds: int) -> int:
        """Get remaining tokens for a key"""
        bucket_key = f"rate_limit:{key}"
        bucket_data = self.cache.get(bucket_key)
        
        if bucket_data is None:
            return limit
        
        current_time = int(time.time())
        time_passed = current_time - bucket_data["last_refill"]
        tokens_to_add = (time_passed * limit) // window_seconds
        
        if tokens_to_add > 0:
            bucket_data["tokens"] = min(limit, bucket_data["tokens"] + tokens_to_add)
            bucket_data["last_refill"] = current_time
            self.cache.set(bucket_key, bucket_data, window_seconds)
        
        return max(0, bucket_data["tokens"])
    
    def reset(self, key: str) -> bool:
        """Reset rate limit for a key"""
        bucket_key = f"rate_limit:{key}"
        return self.cache.delete(bucket_key)

class EmailRateLimiter:
    """Specialized rate limiter for email sending"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
    
    def can_send_email(self, workspace_id: str, prospect_email: str) -> bool:
        """
        Check if we can send an email to a prospect
        
        Implements the 48-hour cooldown rule and hourly rate limiting
        """
        # Check 48-hour cooldown for specific prospect
        cooldown_key = f"email_cooldown:{workspace_id}:{prospect_email}"
        if self.rate_limiter.cache.exists(cooldown_key):
            return False
        
        # Check hourly rate limit for workspace
        rate_key = f"email_rate:{workspace_id}"
        return self.rate_limiter.is_allowed(
            rate_key, 
            settings.rate_limit_emails_per_hour, 
            3600  # 1 hour
        )
    
    def record_email_sent(self, workspace_id: str, prospect_email: str) -> bool:
        """Record that an email was sent to a prospect"""
        # Set 48-hour cooldown
        cooldown_key = f"email_cooldown:{workspace_id}:{prospect_email}"
        cooldown_seconds = settings.email_cooldown_hours * 3600
        return self.rate_limiter.cache.set(cooldown_key, True, cooldown_seconds)
    
    def get_remaining_emails(self, workspace_id: str) -> int:
        """Get remaining emails for workspace this hour"""
        rate_key = f"email_rate:{workspace_id}"
        return self.rate_limiter.get_remaining_tokens(
            rate_key, 
            settings.rate_limit_emails_per_hour, 
            3600
        )

class APIRateLimiter:
    """Rate limiter for API calls"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
    
    def can_make_api_call(self, workspace_id: str) -> bool:
        """Check if workspace can make API call"""
        rate_key = f"api_rate:{workspace_id}"
        return self.rate_limiter.is_allowed(
            rate_key,
            settings.rate_limit_api_calls_per_minute,
            60  # 1 minute
        )
    
    def get_remaining_api_calls(self, workspace_id: str) -> int:
        """Get remaining API calls for workspace this minute"""
        rate_key = f"api_rate:{workspace_id}"
        return self.rate_limiter.get_remaining_tokens(
            rate_key,
            settings.rate_limit_api_calls_per_minute,
            60
        )

# Global rate limiters
email_rate_limiter = EmailRateLimiter()
api_rate_limiter = APIRateLimiter()
