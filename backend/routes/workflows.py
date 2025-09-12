from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from typing import Dict, Any
from services.llm_service import LLMService
import httpx
import os

router = APIRouter()
llm_service = LLMService()

class WorkflowRequest(BaseModel):
    description: str

class WorkflowResponse(BaseModel):
    nodes: list
    connections: dict
    summary: str

class ImportRequest(BaseModel):
    workflow_json: dict

class ImportResponse(BaseModel):
    workflow_id: str
    status: str

@router.post("/generate", response_model=WorkflowResponse)
async def generate_workflow(request: WorkflowRequest):
    """Generate n8n workflow from description"""
    try:
        result = await llm_service.generate_workflow(request.description)
        return WorkflowResponse(
            nodes=result["nodes"],
            connections=result["connections"],
            summary=result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow generation failed: {str(e)}")

@router.post("/import", response_model=ImportResponse)
async def import_workflow(request: ImportRequest):
    """Import workflow to n8n instance"""
    try:
        n8n_base_url = os.getenv("N8N_BASE_URL", "http://n8n:5678")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{n8n_base_url}/api/v1/workflows",
                json=request.workflow_json,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                workflow_data = response.json()
                return ImportResponse(
                    workflow_id=workflow_data.get("id", "unknown"),
                    status="imported"
                )
            else:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"n8n import failed: {response.text}"
                )
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")
