from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, ComplianceCheck, Generation
from pydantic import BaseModel
from typing import List
from services.llm_service import LLMService
import uuid

router = APIRouter()
llm_service = LLMService()

class ComplianceRequest(BaseModel):
    content: str

class ComplianceResponse(BaseModel):
    risk_score: float
    findings: list
    suggested_rewrite: str

class ComplianceCheckResponse(BaseModel):
    id: str
    item_type: str
    item_id: str
    risk_score: float
    issues_json: dict
    resolved: bool
    created_at: str

    class Config:
        from_attributes = True

@router.post("/check", response_model=ComplianceResponse)
async def check_compliance(request: ComplianceRequest):
    """Check content for compliance issues"""
    try:
        result = await llm_service.check_compliance(request.content)
        return ComplianceResponse(
            risk_score=result["risk_score"],
            findings=result["findings"],
            suggested_rewrite=result["suggested_rewrite"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance check failed: {str(e)}")

@router.get("/checks", response_model=List[ComplianceCheckResponse])
async def list_compliance_checks(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List compliance checks"""
    checks = db.query(ComplianceCheck).order_by(ComplianceCheck.created_at.desc()).offset(offset).limit(limit).all()
    
    return [
        ComplianceCheckResponse(
            id=str(c.id),
            item_type=c.item_type,
            item_id=str(c.item_id),
            risk_score=c.risk_score,
            issues_json=c.issues_json,
            resolved=c.resolved,
            created_at=c.created_at.isoformat()
        )
        for c in checks
    ]

@router.get("/checks/{check_id}", response_model=ComplianceCheckResponse)
async def get_compliance_check(check_id: str, db: Session = Depends(get_db)):
    """Get a specific compliance check"""
    check = db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check not found")
    
    return ComplianceCheckResponse(
        id=str(check.id),
        item_type=check.item_type,
        item_id=str(check.item_id),
        risk_score=check.risk_score,
        issues_json=check.issues_json,
        resolved=check.resolved,
        created_at=check.created_at.isoformat()
    )

@router.post("/checks/{check_id}/resolve")
async def resolve_compliance_check(check_id: str, db: Session = Depends(get_db)):
    """Mark a compliance check as resolved"""
    check = db.query(ComplianceCheck).filter(ComplianceCheck.id == check_id).first()
    if not check:
        raise HTTPException(status_code=404, detail="Compliance check not found")
    
    check.resolved = True
    db.commit()
    
    return {"message": "Compliance check resolved"}
