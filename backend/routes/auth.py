"""
Authentication routes for Inno Supps
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.services.auth_service import auth_service
from backend.database import get_db, User, Workspace
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

# Request/Response models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    workspace_name: str

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    workspace_id: str
    csrf_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    workspaces: list

class WorkspaceResponse(BaseModel):
    id: str
    name: str
    slug: str
    role: str

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = auth_service.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    db = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    finally:
        db.close()

# Dependency to get current workspace
async def get_current_workspace(
    request: Request,
    current_user: User = Depends(get_current_user)
) -> str:
    """Get current workspace from header or user's default"""
    workspace_id = request.headers.get("x-workspace-id")
    
    if workspace_id:
        # Verify user has access to this workspace
        if not auth_service.can_read(current_user.id, workspace_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to workspace"
            )
        return workspace_id
    
    # Get user's first workspace as default
    workspaces = auth_service.get_user_workspaces(current_user.id)
    if not workspaces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workspaces found for user"
        )
    
    return str(workspaces[0].id)

@router.post("/signup", response_model=TokenResponse)
async def signup(request: SignupRequest, response: Response):
    """Sign up a new user and create workspace"""
    # Create user
    user = auth_service.create_user(
        email=request.email,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create workspace
    workspace_slug = request.workspace_name.lower().replace(" ", "-")
    workspace = auth_service.create_workspace(
        name=request.workspace_name,
        slug=workspace_slug,
        user_id=str(user.id)
    )
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create workspace"
        )
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "workspace_id": str(workspace.id)}
    )
    
    # Store session
    auth_service.store_session(str(user.id), str(workspace.id), access_token)
    
    # Generate CSRF token
    csrf_token = auth_service.generate_csrf_token()
    
    # Set secure cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400  # 24 hours
    )
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="lax",
        max_age=86400
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        workspace_id=str(workspace.id),
        csrf_token=csrf_token
    )

@router.post("/signin", response_model=TokenResponse)
async def signin(request: SigninRequest, response: Response):
    """Sign in existing user"""
    user = auth_service.authenticate_user(request.email, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user's first workspace
    workspaces = auth_service.get_user_workspaces(user.id)
    if not workspaces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workspaces found for user"
        )
    
    workspace = workspaces[0]
    
    # Create access token
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id), "workspace_id": str(workspace.id)}
    )
    
    # Store session
    auth_service.store_session(str(user.id), str(workspace.id), access_token)
    
    # Generate CSRF token
    csrf_token = auth_service.generate_csrf_token()
    
    # Set secure cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400
    )
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="lax",
        max_age=86400
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        workspace_id=str(workspace.id),
        csrf_token=csrf_token
    )

@router.post("/signout")
async def signout(response: Response, current_user: User = Depends(get_current_user)):
    """Sign out user"""
    # In a real implementation, you'd invalidate the session
    # For now, we'll just clear the cookies
    response.delete_cookie("access_token")
    response.delete_cookie("csrf_token")
    
    return {"message": "Successfully signed out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    workspaces = auth_service.get_user_workspaces(current_user.id)
    workspace_responses = []
    
    for workspace in workspaces:
        role = auth_service.get_user_role_in_workspace(current_user.id, workspace.id)
        workspace_responses.append(WorkspaceResponse(
            id=str(workspace.id),
            name=workspace.name,
            slug=workspace.slug,
            role=role.value if role else "viewer"
        ))
    
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        workspaces=workspace_responses
    )

@router.get("/workspaces", response_model=list[WorkspaceResponse])
async def get_user_workspaces(current_user: User = Depends(get_current_user)):
    """Get all workspaces for current user"""
    workspaces = auth_service.get_user_workspaces(current_user.id)
    workspace_responses = []
    
    for workspace in workspaces:
        role = auth_service.get_user_role_in_workspace(current_user.id, workspace.id)
        workspace_responses.append(WorkspaceResponse(
            id=str(workspace.id),
            name=workspace.name,
            slug=workspace.slug,
            role=role.value if role else "viewer"
        ))
    
    return workspace_responses

@router.post("/switch-workspace/{workspace_id}", response_model=TokenResponse)
async def switch_workspace(
    workspace_id: str,
    current_user: User = Depends(get_current_user),
    response: Response = None
):
    """Switch to a different workspace"""
    # Verify user has access to workspace
    if not auth_service.can_read(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    # Create new access token for workspace
    access_token = auth_service.create_access_token(
        data={"sub": str(current_user.id), "workspace_id": workspace_id}
    )
    
    # Store session
    auth_service.store_session(str(current_user.id), workspace_id, access_token)
    
    # Generate CSRF token
    csrf_token = auth_service.generate_csrf_token()
    
    # Set secure cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=86400
    )
    
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=True,
        samesite="lax",
        max_age=86400
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(current_user.id),
        workspace_id=workspace_id,
        csrf_token=csrf_token
    )