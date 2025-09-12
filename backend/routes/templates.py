from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db, PromptTemplate
from pydantic import BaseModel
from typing import List

router = APIRouter()

class TemplateResponse(BaseModel):
    id: str
    name: str
    version: str
    schema_json: dict
    system_prompt: str
    output_schema: dict
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(db: Session = Depends(get_db)):
    """List all available templates"""
    templates = db.query(PromptTemplate).all()
    
    return [
        TemplateResponse(
            id=str(t.id),
            name=t.name,
            version=t.version,
            schema_json=t.schema_json,
            system_prompt=t.system_prompt,
            output_schema=t.output_schema,
            created_at=t.created_at.isoformat()
        )
        for t in templates
    ]

@router.get("/{template_id}", response_model=TemplateResponse)
async def get_template(template_id: str, db: Session = Depends(get_db)):
    """Get a specific template"""
    template = db.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return TemplateResponse(
        id=str(template.id),
        name=template.name,
        version=template.version,
        schema_json=template.schema_json,
        system_prompt=template.system_prompt,
        output_schema=template.output_schema,
        created_at=template.created_at.isoformat()
    )
