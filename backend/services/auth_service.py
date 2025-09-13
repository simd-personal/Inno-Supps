"""
Authentication service for Inno Supps
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from backend.database import User, Workspace, Membership, MembershipRole, get_db
from backend.config import settings
from backend.services.redis_cache import cache

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = settings.jwt_secret_key
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = settings.jwt_access_token_expire_minutes
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        db = next(get_db())
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None
            if not self.verify_password(password, user.password_hash):
                return None
            if not user.is_active:
                return None
            return user
        finally:
            db.close()
    
    def create_user(self, email: str, password: str, first_name: str, last_name: str) -> Optional[User]:
        """Create a new user"""
        db = next(get_db())
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return None
            
            # Create user
            user = User(
                email=email,
                password_hash=self.get_password_hash(password),
                first_name=first_name,
                last_name=last_name,
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            db.rollback()
            print(f"Error creating user: {e}")
            return None
        finally:
            db.close()
    
    def create_workspace(self, name: str, slug: str, user_id: str) -> Optional[Workspace]:
        """Create a new workspace and add user as admin"""
        db = next(get_db())
        try:
            # Create workspace
            workspace = Workspace(
                name=name,
                slug=slug
            )
            db.add(workspace)
            db.commit()
            db.refresh(workspace)
            
            # Add user as admin
            membership = Membership(
                user_id=user_id,
                workspace_id=workspace.id,
                role=MembershipRole.ADMIN
            )
            db.add(membership)
            db.commit()
            
            return workspace
        except Exception as e:
            db.rollback()
            print(f"Error creating workspace: {e}")
            return None
        finally:
            db.close()
    
    def get_user_workspaces(self, user_id: str) -> list[Workspace]:
        """Get all workspaces for a user"""
        db = next(get_db())
        try:
            memberships = db.query(Membership).filter(Membership.user_id == user_id).all()
            workspaces = [membership.workspace for membership in memberships]
            return workspaces
        finally:
            db.close()
    
    def get_user_role_in_workspace(self, user_id: str, workspace_id: str) -> Optional[MembershipRole]:
        """Get user's role in a specific workspace"""
        db = next(get_db())
        try:
            membership = db.query(Membership).filter(
                Membership.user_id == user_id,
                Membership.workspace_id == workspace_id
            ).first()
            return membership.role if membership else None
        finally:
            db.close()
    
    def can_read(self, user_id: str, workspace_id: str) -> bool:
        """Check if user can read in workspace"""
        role = self.get_user_role_in_workspace(user_id, workspace_id)
        return role is not None
    
    def can_write(self, user_id: str, workspace_id: str) -> bool:
        """Check if user can write in workspace"""
        role = self.get_user_role_in_workspace(user_id, workspace_id)
        return role in [MembershipRole.ADMIN, MembershipRole.CONTRIBUTOR]
    
    def can_admin(self, user_id: str, workspace_id: str) -> bool:
        """Check if user can admin workspace"""
        role = self.get_user_role_in_workspace(user_id, workspace_id)
        return role == MembershipRole.ADMIN
    
    def store_session(self, user_id: str, workspace_id: str, token: str) -> bool:
        """Store session in Redis"""
        session_key = f"session:{token}"
        session_data = {
            "user_id": user_id,
            "workspace_id": workspace_id,
            "created_at": datetime.utcnow().isoformat()
        }
        # Store for 24 hours
        return cache.set(session_key, session_data, 86400)
    
    def get_session(self, token: str) -> Optional[Dict[str, Any]]:
        """Get session from Redis"""
        session_key = f"session:{token}"
        return cache.get(session_key)
    
    def invalidate_session(self, token: str) -> bool:
        """Invalidate session"""
        session_key = f"session:{token}"
        return cache.delete(session_key)
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    def verify_csrf_token(self, token: str, session_token: str) -> bool:
        """Verify CSRF token"""
        # In production, you'd store CSRF tokens in Redis with session association
        # For now, we'll use a simple approach
        return len(token) == 43  # Length of secrets.token_urlsafe(32)

# Global auth service instance
auth_service = AuthService()
