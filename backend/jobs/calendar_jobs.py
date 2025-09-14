"""
Calendar-related background jobs
"""

from typing import Dict, Any
from services.job_service import job
from agents.tools import calendar_find_slots, calendar_book
from database import Meeting, Prospect, get_db
from sqlalchemy.orm import Session

@job(queue_name="default", timeout=300)
def auto_book_meeting(workspace_id: str, prospect_email: str) -> Dict[str, Any]:
    """
    Automatically book a meeting with a prospect
    
    Args:
        workspace_id: Workspace ID
        prospect_email: Prospect email address
    """
    try:
        db = next(get_db())
        try:
            # Find prospect
            prospect = db.query(Prospect).filter(
                Prospect.workspace_id == workspace_id,
                Prospect.email == prospect_email
            ).first()
            
            if not prospect:
                return {
                    "status": "error",
                    "error": "Prospect not found"
                }
            
            # Find available slots
            preferences = {
                "duration": 30,
                "timezone": "UTC",
                "date_range": "next_7_days"
            }
            
            slots = calendar_find_slots(preferences)
            
            if not slots:
                return {
                    "status": "no_slots",
                    "message": "No available slots found"
                }
            
            # Try to book the first available slot
            slot = slots[0]
            booking_result = calendar_book(prospect_email, slot)
            
            if booking_result.get("status") == "success":
                # Create meeting record
                meeting = Meeting(
                    workspace_id=workspace_id,
                    prospect_id=prospect.id,
                    starts_at=slot["start"],
                    ends_at=slot["end"],
                    calendar_link=slot.get("link"),
                    source="auto_booked"
                )
                db.add(meeting)
                db.commit()
                
                return {
                    "status": "success",
                    "meeting_booked": True,
                    "meeting_id": str(meeting.id),
                    "calendar_link": slot.get("link")
                }
            else:
                return {
                    "status": "booking_failed",
                    "error": booking_result.get("error", "Unknown error")
                }
        finally:
            db.close()
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@job(queue_name="low", timeout=180)
def sync_calendar_events(workspace_id: str, integration_id: str) -> Dict[str, Any]:
    """
    Sync calendar events from external provider
    
    Args:
        workspace_id: Workspace ID
        integration_id: Integration ID
    """
    try:
        # In production, this would sync with Google Calendar, Outlook, etc.
        # For now, return mock data
        return {
            "status": "success",
            "events_synced": 0,
            "message": "Calendar sync completed"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
