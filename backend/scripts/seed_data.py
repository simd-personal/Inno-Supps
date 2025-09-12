#!/usr/bin/env python3
"""
Seed script for Inno Supps PromptOps MVP
Creates initial data including users, workspaces, templates, and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, User, Workspace, WorkspaceMembership, PromptTemplate, Generation, KBDoc, ApprovedLanguage
from services.llm_service import LLMService
import json
from datetime import datetime, timedelta
import uuid

def seed_data():
    db = SessionLocal()
    llm_service = LLMService()
    
    try:
        # Create users
        print("Creating users...")
        user1 = User(
            id=uuid.uuid4(),
            email="admin@innosupps.com",
            name="Admin User",
            role="admin"
        )
        user2 = User(
            id=uuid.uuid4(),
            email="marketer@innosupps.com", 
            name="Marketing User",
            role="user"
        )
        db.add_all([user1, user2])
        db.commit()
        
        # Create workspace
        print("Creating workspace...")
        workspace = Workspace(
            id=uuid.uuid4(),
            name="Inno Supps Marketing",
            billing_plan="pro"
        )
        db.add(workspace)
        db.commit()
        
        # Create workspace memberships
        print("Creating workspace memberships...")
        membership1 = WorkspaceMembership(
            user_id=user1.id,
            workspace_id=workspace.id,
            role="admin"
        )
        membership2 = WorkspaceMembership(
            user_id=user2.id,
            workspace_id=workspace.id,
            role="member"
        )
        db.add_all([membership1, membership2])
        db.commit()
        
        # Create prompt templates
        print("Creating prompt templates...")
        templates = [
            PromptTemplate(
                id=uuid.uuid4(),
                name="offer_creator_v1",
                version="1.0",
                schema_json={
                    "type": "object",
                    "properties": {
                        "audience": {"type": "string", "description": "Target audience"},
                        "pain": {"type": "string", "description": "Pain point to address"},
                        "solution": {"type": "string", "description": "Product/solution"},
                        "proof": {"type": "string", "description": "Proof points"},
                        "price": {"type": "string", "description": "Price point"},
                        "guarantee": {"type": "string", "description": "Guarantee offer"}
                    },
                    "required": ["audience", "pain", "solution", "proof", "price", "guarantee"]
                },
                system_prompt="You are an expert copywriter specializing in supplement marketing...",
                output_schema={
                    "type": "object",
                    "properties": {
                        "promise": {"type": "string"},
                        "proof_pillars": {"type": "array", "items": {"type": "string"}},
                        "price": {"type": "string"},
                        "guarantee": {"type": "string"},
                        "cta": {"type": "string"},
                        "landing_blurb": {"type": "string"}
                    }
                }
            ),
            PromptTemplate(
                id=uuid.uuid4(),
                name="cold_email_v1",
                version="1.0",
                schema_json={
                    "type": "object",
                    "properties": {
                        "audience": {"type": "string", "description": "Target audience"},
                        "pain": {"type": "string", "description": "Pain point"},
                        "proof": {"type": "string", "description": "Proof points"},
                        "cta": {"type": "string", "description": "Call to action"}
                    },
                    "required": ["audience", "pain", "proof", "cta"]
                },
                system_prompt="You are an expert cold email writer for supplement marketing...",
                output_schema={
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "body": {"type": "string"},
                        "tone": {"type": "string"},
                        "compliance_notes": {"type": "string"}
                    }
                }
            ),
            PromptTemplate(
                id=uuid.uuid4(),
                name="ad_writer_v1",
                version="1.0",
                schema_json={
                    "type": "object",
                    "properties": {
                        "channel": {"type": "string", "description": "Advertising channel"},
                        "audience": {"type": "string", "description": "Target audience"},
                        "pain_or_benefit": {"type": "string", "description": "Pain point or benefit"}
                    },
                    "required": ["channel", "audience", "pain_or_benefit"]
                },
                system_prompt="You are an expert ad copywriter for supplement marketing...",
                output_schema={
                    "type": "object",
                    "properties": {
                        "proof_based": {"type": "object"},
                        "transformation": {"type": "object"},
                        "social_proof": {"type": "object"}
                    }
                }
            ),
            PromptTemplate(
                id=uuid.uuid4(),
                name="workflow_from_prompt_v1",
                version="1.0",
                schema_json={
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "Workflow description"}
                    },
                    "required": ["description"]
                },
                system_prompt="You are an expert n8n workflow designer...",
                output_schema={
                    "type": "object",
                    "properties": {
                        "nodes": {"type": "array"},
                        "connections": {"type": "object"},
                        "summary": {"type": "string"}
                    }
                }
            )
        ]
        
        db.add_all(templates)
        db.commit()
        
        # Create approved language entries
        print("Creating approved language entries...")
        approved_language = [
            ApprovedLanguage(
                id=uuid.uuid4(),
                category="fat_loss",
                text="Supports healthy weight management when combined with diet and exercise",
                citations=["FDA 21 CFR 101.93"]
            ),
            ApprovedLanguage(
                id=uuid.uuid4(),
                category="muscle_building",
                text="Supports muscle recovery and growth when combined with resistance training",
                citations=["FDA 21 CFR 101.93"]
            ),
            ApprovedLanguage(
                id=uuid.uuid4(),
                category="energy",
                text="Supports natural energy levels and mental focus",
                citations=["FDA 21 CFR 101.93"]
            )
        ]
        
        db.add_all(approved_language)
        db.commit()
        
        # Create sample generations
        print("Creating sample generations...")
        sample_generations = [
            Generation(
                id=uuid.uuid4(),
                template_id=templates[0].id,  # offer_creator_v1
                user_id=user1.id,
                workspace_id=workspace.id,
                inputs_json={
                    "audience": "busy professionals aged 30-50",
                    "pain": "struggling with weight loss despite dieting",
                    "solution": "fat loss supplement with natural ingredients",
                    "proof": "clinical studies, 10,000+ customers, 30-day guarantee",
                    "price": "$97 with 50% discount",
                    "guarantee": "30-day money-back guarantee"
                },
                output_json={
                    "promise": "Finally Lose Stubborn Belly Fat in 30 Days - Guaranteed",
                    "proof_pillars": [
                        "Clinical study shows 12% more fat loss",
                        "10,000+ customers lost 15+ lbs",
                        "30-day money-back guarantee"
                    ],
                    "price": "$97 (50% off - Limited Time)",
                    "guarantee": "30-day money-back guarantee",
                    "cta": "Start Your Transformation Today",
                    "landing_blurb": "Join thousands who've finally lost stubborn belly fat with our clinically-proven formula. 30-day guarantee."
                },
                score=0.85,
                compliance_risk=0.2,
                status="completed",
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            Generation(
                id=uuid.uuid4(),
                template_id=templates[1].id,  # cold_email_v1
                user_id=user2.id,
                workspace_id=workspace.id,
                inputs_json={
                    "audience": "fitness enthusiasts",
                    "pain": "plateau in muscle gains",
                    "proof": "proven formula, 5-star reviews",
                    "cta": "schedule a consultation"
                },
                output_json={
                    "subject": "Break Through Your Muscle Plateau",
                    "body": "Hi [Name], I noticed you're serious about fitness but hitting a plateau. Our clients typically see 20% more gains in 8 weeks. Want to learn how?",
                    "tone": "professional but friendly",
                    "compliance_notes": "Avoid specific claims about muscle growth percentages"
                },
                score=0.78,
                compliance_risk=0.3,
                status="completed",
                created_at=datetime.utcnow() - timedelta(hours=6)
            )
        ]
        
        db.add_all(sample_generations)
        db.commit()
        
        # Create knowledge base documents
        print("Creating knowledge base documents...")
        kb_docs = [
        KBDoc(
            id=uuid.uuid4(),
            source="fda_guidelines",
            title="FDA Guidelines for Supplement Claims",
            url="https://www.fda.gov/food/dietary-supplements",
            text="FDA guidelines state that supplement claims must be truthful and not misleading. Structure/function claims are allowed but disease claims are prohibited.",
            meta_data={"category": "compliance", "importance": "high"}
        ),
        KBDoc(
            id=uuid.uuid4(),
            source="ftc_guidelines",
            title="FTC Guidelines for Advertising",
            url="https://www.ftc.gov/news-events/topics/truth-advertising",
            text="FTC requires that all advertising claims be substantiated with competent and reliable scientific evidence.",
            meta_data={"category": "compliance", "importance": "high"}
        )
        ]
        
        db.add_all(kb_docs)
        db.commit()
        
        print("✅ Seed data created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
