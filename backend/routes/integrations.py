"""
Integration management routes for Inno Supps
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from pydantic import BaseModel
from services.integration_service import integration_service
from services.auth_service import auth_service, get_current_user, get_current_workspace
from database import User, IntegrationType

router = APIRouter(prefix="/integrations", tags=["integrations"])

# Request/Response models
class CreateIntegrationRequest(BaseModel):
    type: str
    auth_data: Dict[str, Any]

class UpdateIntegrationRequest(BaseModel):
    auth_data: Dict[str, Any]

class IntegrationResponse(BaseModel):
    id: str
    type: str
    status: str
    provider_status: str
    connected: bool
    created_at: str

@router.get("/available")
async def get_available_integrations():
    """Get list of available integration types"""
    return {"integrations": integration_service.get_available_integrations()}

@router.get("/status")
async def get_integration_status(
    current_user: User = Depends(get_current_user),
    workspace_id: str = Depends(get_current_workspace)
):
    """Get status of all integrations for workspace"""
    status = integration_service.get_integration_status(workspace_id)
    return {"integrations": status}

@router.post("/create")
async def create_integration(
    request: CreateIntegrationRequest,
    current_user: User = Depends(get_current_user),
    workspace_id: str = Depends(get_current_workspace)
):
    """Create new integration"""
    # Verify user can write to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    try:
        integration_type = IntegrationType(request.type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid integration type: {request.type}"
        )
    
    result = integration_service.create_integration(
        workspace_id, integration_type, request.auth_data
    )
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result

@router.put("/{integration_id}")
async def update_integration(
    integration_id: str,
    request: UpdateIntegrationRequest,
    current_user: User = Depends(get_current_user),
    workspace_id: str = Depends(get_current_workspace)
):
    """Update integration auth data"""
    # Verify user can write to workspace
    if not auth_service.can_write(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    result = integration_service.update_integration(
        workspace_id, integration_id, request.auth_data
    )
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result

@router.post("/{integration_id}/test")
async def test_integration(
    integration_id: str,
    current_user: User = Depends(get_current_user),
    workspace_id: str = Depends(get_current_workspace)
):
    """Test integration connection"""
    # Verify user can read workspace
    if not auth_service.can_read(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    result = integration_service.test_integration(workspace_id, integration_id)
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result

@router.delete("/{integration_id}")
async def delete_integration(
    integration_id: str,
    current_user: User = Depends(get_current_user),
    workspace_id: str = Depends(get_current_workspace)
):
    """Delete integration"""
    # Verify user can admin workspace
    if not auth_service.can_admin(current_user.id, workspace_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to workspace"
        )
    
    result = integration_service.delete_integration(workspace_id, integration_id)
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    
    return result

@router.get("/{integration_type}/test-connection")
async def test_connection_type(
    integration_type: str,
    auth_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Test connection for integration type without saving"""
    try:
        integration_type_enum = IntegrationType(integration_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid integration type: {integration_type}"
        )
    
    provider = integration_service.get_provider(integration_type_enum, auth_data)
    is_connected = provider.test_connection()
    
    return {
        "connected": is_connected,
        "provider_status": provider.get_status(),
        "integration_type": integration_type
    }
