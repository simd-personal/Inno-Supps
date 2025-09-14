"""
Research-related background jobs
"""

from typing import Dict, Any
from services.job_service import job
from agents.tools import generate_niche_report, generate_growth_plan
from database import ResearchBrief, GrowthPlan, get_db
from sqlalchemy.orm import Session

@job(queue_name="low", timeout=1800)  # 30 minutes for research
def run_niche_research(workspace_id: str, research_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run comprehensive niche research
    
    Args:
        workspace_id: Workspace ID
        research_inputs: Research parameters
    """
    try:
        keywords = research_inputs.get("keywords", [])
        region = research_inputs.get("region", "US")
        size_range = research_inputs.get("size_range", "1-50")
        
        # Generate niche report
        report_md = generate_niche_report(keywords, region, size_range)
        
        # Create research brief record
        db = next(get_db())
        try:
            research_brief = ResearchBrief(
                workspace_id=workspace_id,
                inputs_json=research_inputs,
                output_md=report_md
            )
            db.add(research_brief)
            db.commit()
            db.refresh(research_brief)
            
            return {
                "status": "success",
                "research_brief_id": str(research_brief.id),
                "report_length": len(report_md),
                "keywords": keywords
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="low", timeout=1200)  # 20 minutes for growth plan
def create_growth_plan(workspace_id: str, plan_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create comprehensive growth plan
    
    Args:
        workspace_id: Workspace ID
        plan_inputs: Growth plan parameters
    """
    try:
        # Generate growth plan
        plan_result = generate_growth_plan(plan_inputs)
        
        # Create growth plan record
        db = next(get_db())
        try:
            growth_plan = GrowthPlan(
                workspace_id=workspace_id,
                inputs_json=plan_inputs,
                plan_md=plan_result.get("plan_md", ""),
                kpis_json=plan_result.get("kpis_json", {})
            )
            db.add(growth_plan)
            db.commit()
            db.refresh(growth_plan)
            
            return {
                "status": "success",
                "growth_plan_id": str(growth_plan.id),
                "plan_length": len(plan_result.get("plan_md", "")),
                "kpis": plan_result.get("kpis_json", {})
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="default", timeout=600)
def enrich_prospect_data(workspace_id: str, prospect_id: str) -> Dict[str, Any]:
    """
    Enrich prospect data with external sources
    
    Args:
        workspace_id: Workspace ID
        prospect_id: Prospect ID
    """
    try:
        db = next(get_db())
        try:
            # Get prospect
            prospect = db.query(Prospect).filter(
                Prospect.workspace_id == workspace_id,
                Prospect.id == prospect_id
            ).first()
            
            if not prospect:
                return {
                    "status": "error",
                    "error": "Prospect not found"
                }
            
            # In production, this would call enrichment APIs
            # For now, generate mock enrichment data
            enrichment_data = {
                "company_size": "50-200 employees",
                "industry": "Technology",
                "revenue_range": "$10M-$50M",
                "linkedin_url": f"https://linkedin.com/company/{prospect.company.lower().replace(' ', '-')}",
                "website": f"https://{prospect.company.lower().replace(' ', '')}.com",
                "social_media": {
                    "twitter": f"@{prospect.company.lower().replace(' ', '')}",
                    "linkedin": f"https://linkedin.com/company/{prospect.company.lower().replace(' ', '-')}"
                },
                "technologies": ["React", "Node.js", "AWS", "PostgreSQL"],
                "funding": {
                    "total_raised": "$5M",
                    "last_round": "Series A",
                    "investors": ["Accel", "Sequoia"]
                }
            }
            
            # Update prospect with enrichment data
            prospect.enrichment_json = enrichment_data
            prospect.score = 85  # Mock score
            db.commit()
            
            return {
                "status": "success",
                "prospect_id": str(prospect.id),
                "enrichment_data": enrichment_data,
                "score": 85
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
