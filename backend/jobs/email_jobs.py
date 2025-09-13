"""
Email-related background jobs
"""

from typing import Dict, Any
from backend.services.job_service import job
from backend.agents.tools import classify_intent, draft_email
from backend.database import Thread, Message, MessageDirection, get_db
from backend.services.rate_limiter import email_rate_limiter
from backend.services.llm_service import LLMService
from sqlalchemy.orm import Session

llm_service = LLMService()

@job(queue_name="default", timeout=300)
def ingest_email(workspace_id: str, email_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ingest and classify an inbound email
    
    Args:
        workspace_id: Workspace ID
        email_data: Email data from provider
    """
    try:
        # Extract email content
        subject = email_data.get("subject", "")
        body = email_data.get("body", "")
        from_email = email_data.get("from_email", "")
        to_email = email_data.get("to_email", "")
        thread_id = email_data.get("thread_id")
        
        # Classify email intent
        intent_result = classify_intent(body)
        
        # Create or update thread
        db = next(get_db())
        try:
            thread = db.query(Thread).filter(
                Thread.workspace_id == workspace_id,
                Thread.provider_thread_id == thread_id
            ).first()
            
            if not thread:
                thread = Thread(
                    workspace_id=workspace_id,
                    provider_thread_id=thread_id,
                    subject=subject
                )
                db.add(thread)
                db.commit()
                db.refresh(thread)
            
            # Create message record
            message = Message(
                thread_id=thread.id,
                provider_message_id=email_data.get("message_id", ""),
                direction=MessageDirection.INBOUND,
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                body_text=body,
                headers_json=email_data.get("headers", {})
            )
            db.add(message)
            db.commit()
            
            # If positive intent, trigger SDR reply job
            if intent_result.get("reply_type") == "positive":
                sdr_reply.delay(workspace_id, str(thread.id), intent_result)
            
            return {
                "status": "success",
                "thread_id": str(thread.id),
                "intent": intent_result
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="high", timeout=600)
def sdr_reply(workspace_id: str, thread_id: str, intent_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate SDR suggested reply and schedule booking attempts
    
    Args:
        workspace_id: Workspace ID
        thread_id: Thread ID
        intent_data: Intent classification results
    """
    try:
        db = next(get_db())
        try:
            # Get thread and latest message
            thread = db.query(Thread).filter(
                Thread.workspace_id == workspace_id,
                Thread.id == thread_id
            ).first()
            
            if not thread:
                return {"status": "error", "error": "Thread not found"}
            
            latest_message = db.query(Message).filter(
                Message.thread_id == thread_id
            ).order_by(Message.created_at.desc()).first()
            
            if not latest_message:
                return {"status": "error", "error": "No messages found"}
            
            # Generate reply context
            context = {
                "prospect_email": latest_message.from_email,
                "original_subject": latest_message.subject,
                "original_body": latest_message.body_text,
                "intent": intent_data,
                "workspace_id": workspace_id
            }
            
            # Draft reply email
            reply_data = draft_email(context, "professional")
            
            # If they want to book a meeting, schedule auto-booking
            if intent_data.get("book_meeting", False):
                auto_book_meeting.delay(workspace_id, latest_message.from_email)
            
            return {
                "status": "success",
                "suggested_reply": reply_data,
                "auto_booking_scheduled": intent_data.get("book_meeting", False)
            }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="low", timeout=180)
def send_email(workspace_id: str, prospect_email: str, email_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send an email to a prospect
    
    Args:
        workspace_id: Workspace ID
        prospect_email: Prospect email address
        email_data: Email content and metadata
    """
    try:
        # Check rate limits
        if not email_rate_limiter.can_send_email(workspace_id, prospect_email):
            return {
                "status": "rate_limited",
                "error": "Rate limit exceeded for this prospect"
            }
        
        # In production, this would integrate with email providers
        # For now, we'll simulate sending
        print(f"Sending email to {prospect_email}: {email_data.get('subject', 'No subject')}")
        
        # Record email sent
        email_rate_limiter.record_email_sent(workspace_id, prospect_email)
        
        return {
            "status": "success",
            "message": "Email sent successfully",
            "prospect_email": prospect_email
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
