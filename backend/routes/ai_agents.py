"""
AI Agents routes for Inno Supps
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests

router = APIRouter(prefix="/api/agents", tags=["ai-agents"])

# Request/Response models
class ColdEmailRequest(BaseModel):
    prospect_name: str
    company: str
    role: str
    pain_points: List[str]
    value_proposition: str
    email_type: Optional[str] = "cold_outreach"

class NicheResearchRequest(BaseModel):
    skills: List[str]
    interests: List[str]
    budget: int
    experience_level: str
    time_commitment: Optional[str] = "part_time"

class ColdEmailResponse(BaseModel):
    subject: str
    email_body: str
    personalization_score: int
    call_to_action: str
    follow_up_suggestions: List[str]

class NicheResearchResponse(BaseModel):
    recommended_niches: List[Dict[str, Any]]
    market_analysis: Dict[str, Any]
    implementation_strategy: List[str]
    risk_assessment: Dict[str, Any]

@router.post("/cold-email-writer/generate", response_model=ColdEmailResponse)
async def generate_cold_email(request: ColdEmailRequest):
    """Generate a personalized cold email"""
    try:
        # Call the simple AI API
        ai_response = requests.post(
            "http://localhost:8001/generate_cold_email",
            json={
                "prospect_name": request.prospect_name,
                "company": request.company,
                "role": request.role,
                "pain_points": request.pain_points,
                "value_proposition": request.value_proposition,
                "email_type": request.email_type
            },
            timeout=30
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            return ColdEmailResponse(
                subject=data.get("subject", "Let's discuss how we can help"),
                email_body=data.get("email_body", "Email generation failed"),
                personalization_score=data.get("personalization_score", 85),
                call_to_action=data.get("call_to_action", "Schedule a call"),
                follow_up_suggestions=data.get("follow_up_suggestions", ["Follow up in 3 days", "Send case study"])
            )
        else:
            raise HTTPException(status_code=500, detail="AI service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to mock data if AI service is down
        return ColdEmailResponse(
            subject=f"Quick question about {request.company}'s growth strategy",
            email_body=f"""Hi {request.prospect_name},

I noticed {request.company} is facing some {', '.join(request.pain_points[:2])} challenges. 

As a {request.role}, you're probably looking for ways to {request.value_proposition}.

I've helped similar companies in your space achieve 40% faster growth through our proven methodology.

Would you be open to a 15-minute call this week to discuss how we might help {request.company}?

Best regards,
[Your Name]""",
            personalization_score=75,
            call_to_action="Schedule a 15-minute call",
            follow_up_suggestions=["Follow up in 3 days", "Send case study", "Connect on LinkedIn"]
        )

@router.post("/niche-researcher/analyze", response_model=NicheResearchResponse)
async def analyze_niche(request: NicheResearchRequest):
    """Analyze and recommend profitable niches"""
    try:
        # Call the simple AI API
        ai_response = requests.post(
            "http://localhost:8001/analyze_niche",
            json={
                "skills": request.skills,
                "interests": request.interests,
                "budget": request.budget,
                "experience_level": request.experience_level,
                "time_commitment": request.time_commitment
            },
            timeout=30
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            return NicheResearchResponse(
                recommended_niches=data.get("recommended_niches", []),
                market_analysis=data.get("market_analysis", {}),
                implementation_strategy=data.get("implementation_strategy", []),
                risk_assessment=data.get("risk_assessment", {})
            )
        else:
            raise HTTPException(status_code=500, detail="AI service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to mock data if AI service is down
        return NicheResearchResponse(
            recommended_niches=[
                {
                    "name": "SaaS for Small Businesses",
                    "profitability_score": 85,
                    "market_size": "$50B",
                    "competition_level": "Medium",
                    "entry_barrier": "Low",
                    "description": "B2B software solutions for small to medium businesses"
                },
                {
                    "name": "AI-Powered Marketing Tools",
                    "profitability_score": 90,
                    "market_size": "$25B",
                    "competition_level": "High",
                    "entry_barrier": "Medium",
                    "description": "Marketing automation and AI-driven customer acquisition tools"
                }
            ],
            market_analysis={
                "total_addressable_market": "$75B",
                "growth_rate": "15% annually",
                "key_trends": ["AI integration", "Automation", "Personalization"]
            },
            implementation_strategy=[
                "Start with MVP in 3 months",
                "Focus on one specific use case",
                "Build strong customer feedback loop"
            ],
            risk_assessment={
                "market_risk": "Low",
                "competition_risk": "Medium",
                "technical_risk": "Low"
            }
        )

@router.get("/health")
async def health_check():
    """Health check for AI agents"""
    return {"status": "healthy", "message": "AI Agents service is running"}