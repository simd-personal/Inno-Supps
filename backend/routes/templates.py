from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, EmailTemplate
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TemplateResponse(BaseModel):
    id: str
    name: str
    subject: str
    body_md: str
    variables_json: dict
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(db: Session = Depends(get_db)):
    """List all available templates"""
    templates = db.query(EmailTemplate).all()
    
    return [
        TemplateResponse(
            id=str(t.id),
            name=t.name,
            subject=t.subject or "",
            body_md=t.body_md or "",
            variables_json=t.variables_json or {},
            created_at=t.created_at.isoformat()
        )
        for t in templates
    ]

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific template"""
    template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return TemplateResponse(
        id=str(template.id),
        name=template.name,
        subject=template.subject or "",
        body_md=template.body_md or "",
        variables_json=template.variables_json or {},
        created_at=template.created_at.isoformat()
    )