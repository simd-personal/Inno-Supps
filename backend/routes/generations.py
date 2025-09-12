from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db, Generation, PromptTemplate, User
from pydantic import BaseModel
from typing import List, Optional
import uuid
from services.llm_service import LLMService
from services.redis_service import RedisService

router = APIRouter()
llm_service = LLMService()
redis_service = RedisService()

class GenerationRequest(BaseModel):
    template_id: str
    inputs: dict

class GenerationResponse(BaseModel):
    id: str
    template_id: str
    inputs: dict
    output: dict
    score: Optional[float]
    compliance_risk: Optional[float]
    status: str
    created_at: str

    class Config:
        from_attributes = True

class ScoreRequest(BaseModel):
    content: str

class ScoreResponse(BaseModel):
    clarity: float
    specificity: float
    compliance: float
    brand_match: float

@router.post("/generate", response_model=GenerationResponse)
async def generate_content(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate content using a template"""
    # Get template
    template = db.query(PromptTemplate).filter(PromptTemplate.id == request.template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Get user (simplified for MVP)
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate content based on template
    try:
        if template.name == "offer_creator_v1":
            output = await llm_service.generate_offer_creator(request.inputs)
        elif template.name == "cold_email_v1":
            output = await llm_service.generate_cold_email(request.inputs)
        elif template.name == "ad_writer_v1":
            output = await llm_service.generate_ad_variants(request.inputs)
        else:
            raise HTTPException(status_code=400, detail="Unknown template")
        
        # Create generation record
        generation = Generation(
            template_id=request.template_id,
            user_id=user.id,
            workspace_id=user.workspace_memberships[0].workspace_id if user.workspace_memberships else None,
            inputs_json=request.inputs,
            output_json=output,
            status="completed"
        )
        db.add(generation)
        db.commit()
        db.refresh(generation)
        
        # Schedule compliance check
        background_tasks.add_task(check_compliance_async, str(generation.id))
        
        return GenerationResponse(
            id=str(generation.id),
            template_id=str(generation.template_id),
            inputs=generation.inputs_json,
            output=generation.output_json,
            score=generation.score,
            compliance_risk=generation.compliance_risk,
            status=generation.status,
            created_at=generation.created_at.isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.post("/score", response_model=ScoreResponse)
async def score_content(request: ScoreRequest):
    """Score content on various rubrics"""
    try:
        scores = await llm_service.score_content(request.content)
        return ScoreResponse(**scores)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

@router.get("/{generation_id}", response_model=GenerationResponse)
async def get_generation(generation_id: str, db: Session = Depends(get_db)):
    """Get a specific generation"""
    generation = db.query(Generation).filter(Generation.id == generation_id).first()
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return GenerationResponse(
        id=str(generation.id),
        template_id=str(generation.template_id),
        inputs=generation.inputs_json,
        output=generation.output_json,
        score=generation.score,
        compliance_risk=generation.compliance_risk,
        status=generation.status,
        created_at=generation.created_at.isoformat()
    )

@router.get("/", response_model=List[GenerationResponse])
async def list_generations(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List recent generations"""
    generations = db.query(Generation).order_by(Generation.created_at.desc()).offset(offset).limit(limit).all()
    
    return [
        GenerationResponse(
            id=str(g.id),
            template_id=str(g.template_id),
            inputs=g.inputs_json,
            output=g.output_json,
            score=g.score,
            compliance_risk=g.compliance_risk,
            status=g.status,
            created_at=g.created_at.isoformat()
        )
        for g in generations
    ]

async def check_compliance_async(generation_id: str):
    """Background task to check compliance"""
    # This would be implemented to check compliance and update the generation
    pass
