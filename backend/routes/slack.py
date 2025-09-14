from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
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
    """Handle Slack slash commands (mock implementation)"""
    form_data = await request.form()
    command = SlackCommand(**form_data)
    
    if command.command == "/inno":
        if command.text == "summary today":
            return await generate_daily_summary()
        else:
            return {"text": "Unknown command. Try `/inno summary today`"}
    
    return {"text": "Unknown command"}

@router.post("/webhook")
async def send_slack_message(message: SlackMessage):
    """Send message to Slack webhook (mock implementation)"""
    return {"status": "sent"}

async def generate_daily_summary() -> dict:
    """Generate daily summary for Slack (mock implementation)"""
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
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "1. *Fat Loss Pro* - ROAS: 4.2x, Margin: 60%, Adj ROAS: 2.52x"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "2. *Muscle Builder* - ROAS: 3.8x, Margin: 55%, Adj ROAS: 2.09x"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "3. *Energy Boost* - ROAS: 5.1x, Margin: 70%, Adj ROAS: 3.57x"
            }
        }
    ]
    
    return {
        "response_type": "in_channel",
        "blocks": blocks
    }