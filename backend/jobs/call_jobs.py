"""
Call-related background jobs
"""

from typing import Dict, Any
from services.job_service import job
from agents.tools import analyze_transcript
from database import Call, Prospect, get_db
from services.llm_service import LLMService
from sqlalchemy.orm import Session

llm_service = LLMService()

@job(queue_name="high", timeout=1800)  # 30 minutes for transcription
def transcribe_and_analyze_call(workspace_id: str, recording_url: str, prospect_id: str = None) -> Dict[str, Any]:
    """
    Transcribe call recording and analyze for insights
    
    Args:
        workspace_id: Workspace ID
        recording_url: URL of the recording
        prospect_id: Optional prospect ID
    """
    try:
        # In production, this would use OpenAI Whisper or similar
        # For now, generate mock transcript
        mock_transcript = """
        [00:00] Hello, this is John from TechCorp. Thanks for taking my call.
        [00:05] Hi John, this is Sarah. What can I help you with today?
        [00:10] We're looking for a solution to help with our lead generation process.
        [00:15] That's great! We specialize in exactly that. Can you tell me more about your current process?
        [00:20] Right now we're using spreadsheets and it's getting out of hand.
        [00:25] I understand. How many leads are you processing per month?
        [00:30] About 500-1000 leads, but we're only converting about 5%.
        [00:35] That's actually quite common. Our clients typically see 15-20% conversion rates.
        [00:40] That sounds promising. What's the investment like?
        [00:45] Our packages start at $2,000/month for up to 1,000 leads.
        [00:50] That's within our budget. When could we get started?
        [00:55] We could have you up and running within 2 weeks. Would you like to schedule a demo?
        [01:00] Yes, that would be great. How about next Tuesday at 2pm?
        [01:05] Perfect! I'll send you a calendar invite. Thanks for your time today.
        [01:10] Thank you, Sarah. Looking forward to the demo.
        """
        
        # Analyze transcript
        analysis = analyze_transcript(mock_transcript)
        
        # Create call record
        db = next(get_db())
        try:
            call = Call(
                workspace_id=workspace_id,
                prospect_id=prospect_id,
                recording_url=recording_url,
                transcript_text=mock_transcript,
                analysis_json=analysis
            )
            db.add(call)
            db.commit()
            db.refresh(call)
            
            return {
                "status": "success",
                "call_id": str(call.id),
                "transcript_length": len(mock_transcript),
                "analysis": analysis
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="default", timeout=300)
def process_zoom_webhook(workspace_id: str, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process Zoom webhook for call recordings
    
    Args:
        workspace_id: Workspace ID
        webhook_data: Zoom webhook payload
    """
    try:
        # Extract recording URL from webhook
        recording_url = webhook_data.get("recording_url")
        if not recording_url:
            return {
                "status": "error",
                "error": "No recording URL in webhook"
            }
        
        # Trigger transcription job
        job_id = transcribe_and_analyze_call.delay(workspace_id, recording_url)
        
        return {
            "status": "success",
            "transcription_job_id": job_id,
            "recording_url": recording_url
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
