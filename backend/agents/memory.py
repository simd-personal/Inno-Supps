"""
Agent memory interface backed by Postgres
"""

from typing import Any, Optional, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from backend.database import AgentMemory as AgentMemoryModel, get_db
from backend.config import settings

class AgentMemory:
    def __init__(self, workspace_id: str, user_id: Optional[str] = None):
        self.workspace_id = workspace_id
        self.user_id = user_id
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from memory"""
        db = next(get_db())
        try:
            memory = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.user_id == self.user_id,
                AgentMemoryModel.key == key,
                AgentMemoryModel.expires_at > datetime.utcnow()
            ).first()
            
            if memory:
                return memory.value_json
            return None
        finally:
            db.close()
    
    def set(self, key: str, value: Any, ttl_hours: Optional[int] = None) -> bool:
        """Set value in memory with optional TTL"""
        db = next(get_db())
        try:
            expires_at = None
            if ttl_hours:
                expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)
            
            # Check if key already exists
            existing = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.user_id == self.user_id,
                AgentMemoryModel.key == key
            ).first()
            
            if existing:
                existing.value_json = value
                existing.expires_at = expires_at
            else:
                memory = AgentMemoryModel(
                    workspace_id=self.workspace_id,
                    user_id=self.user_id,
                    key=key,
                    value_json=value,
                    expires_at=expires_at
                )
                db.add(memory)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Memory set error: {e}")
            return False
        finally:
            db.close()
    
    def delete(self, key: str) -> bool:
        """Delete key from memory"""
        db = next(get_db())
        try:
            memory = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.user_id == self.user_id,
                AgentMemoryModel.key == key
            ).first()
            
            if memory:
                db.delete(memory)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Memory delete error: {e}")
            return False
        finally:
            db.close()
    
    def list_keys(self) -> List[str]:
        """List all keys in memory"""
        db = next(get_db())
        try:
            memories = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.user_id == self.user_id,
                AgentMemoryModel.expires_at > datetime.utcnow()
            ).all()
            
            return [memory.key for memory in memories]
        finally:
            db.close()
    
    def clear_expired(self) -> int:
        """Clear expired memories and return count"""
        db = next(get_db())
        try:
            count = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.expires_at < datetime.utcnow()
            ).delete()
            
            db.commit()
            return count
        except Exception as e:
            db.rollback()
            print(f"Memory clear expired error: {e}")
            return 0
        finally:
            db.close()
    
    def clear_all(self) -> int:
        """Clear all memories for workspace/user and return count"""
        db = next(get_db())
        try:
            count = db.query(AgentMemoryModel).filter(
                AgentMemoryModel.workspace_id == self.workspace_id,
                AgentMemoryModel.user_id == self.user_id
            ).delete()
            
            db.commit()
            return count
        except Exception as e:
            db.rollback()
            print(f"Memory clear all error: {e}")
            return 0
        finally:
            db.close()
