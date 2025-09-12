from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db, Generation, ComplianceCheck
from pydantic import BaseModel
from typing import List
import json
from datetime import datetime, timedelta

router = APIRouter()

class SlackCommand(BaseModel):
    token: str
    team_id: str
    team_domain: str
    channel_id: str
    channel_name: str
    user_id: str
    user_name: str
    command: str
    text: str
    response_url: str
    trigger_id: str

class SlackMessage(BaseModel):
    text: str
    blocks: List[dict] = []

@router.post("/command")
async def handle_slack_command(request: Request, db: Session = Depends(get_db)):
    """Handle Slack slash commands"""
    form_data = await request.form()
    command = SlackCommand(**form_data)
    
    if command.command == "/inno":
        if command.text == "summary today":
            return await generate_daily_summary(db)
        else:
            return {"text": "Unknown command. Try `/inno summary today`"}
    
    return {"text": "Unknown command"}

@router.post("/webhook")
async def send_slack_message(message: SlackMessage):
    """Send message to Slack webhook"""
    # This would integrate with Slack webhook URL
    return {"status": "sent"}

async def generate_daily_summary(db: Session) -> dict:
    """Generate daily summary for Slack"""
    # Get recent generations
    recent_generations = db.query(Generation).order_by(Generation.created_at.desc()).limit(3).all()
    
    # Get high-risk compliance checks
    high_risk_checks = db.query(ComplianceCheck).filter(
        ComplianceCheck.risk_score > 0.7,
        ComplianceCheck.resolved == False
    ).limit(5).all()
    
    # Mock ad stats (in real implementation, this would come from analytics)
    mock_ad_stats = [
        {"campaign": "Fat Loss Pro", "roas": 4.2, "margin": 0.6, "adjusted_roas": 2.52},
        {"campaign": "Muscle Builder", "roas": 3.8, "margin": 0.55, "adjusted_roas": 2.09},
        {"campaign": "Energy Boost", "roas": 5.1, "margin": 0.7, "adjusted_roas": 3.57}
    ]
    
    # Sort by adjusted ROAS
    mock_ad_stats.sort(key=lambda x: x["adjusted_roas"], reverse=True)
    
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "📊 Daily Inno Supps Summary"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🏆 Top Performing Campaigns (by Adjusted ROAS)*"
            }
        }
    ]
    
    # Add top campaigns
    for i, stat in enumerate(mock_ad_stats[:3], 1):
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{i}. *{stat['campaign']}* - ROAS: {stat['roas']}x, Margin: {stat['margin']*100:.0f}%, Adj ROAS: {stat['adjusted_roas']:.2f}x"
            }
        })
    
    # Add recent generations
    if recent_generations:
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*📝 Recent Generations*"
                }
            }
        ])
        
        for gen in recent_generations:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"• {gen.template.name} - {gen.created_at.strftime('%H:%M')} - Status: {gen.status}"
                }
            })
    
    # Add compliance alerts
    if high_risk_checks:
        blocks.extend([
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*⚠️ High Risk Compliance Flags*"
                }
            }
        ])
        
        for check in high_risk_checks:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"• Risk Score: {check.risk_score:.2f} - {check.item_type} - {len(check.issues_json.get('issues', []))} issues"
                }
            })
    
    return {
        "response_type": "in_channel",
        "blocks": blocks
    }
