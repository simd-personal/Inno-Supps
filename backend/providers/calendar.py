"""
Calendar providers (Google Calendar, Outlook, Calendly)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base import BaseProvider
from config import settings

class GoogleCalendarProvider(BaseProvider):
    """Google Calendar integration provider"""
    
    def test_connection(self) -> bool:
        if self.mock_mode:
            return True
        
        # In production, test Google Calendar API connection
        try:
            # This would use Google Calendar API to test connection
            return True
        except Exception:
            return False
    
    def get_status(self) -> str:
        if self.mock_mode:
            return "connected (mock)"
        return "connected" if self.test_connection() else "disconnected"
    
    def list_free_busy(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """List free/busy times"""
        if self.mock_mode:
            return self._get_mock_free_busy(start_time, end_time)
        
        # In production, use Google Calendar API
        return []
    
    def create_event(self, title: str, start_time: datetime, end_time: datetime, 
                    attendees: List[str] = None, description: str = None) -> Dict[str, Any]:
        """Create calendar event"""
        if self.mock_mode:
            return {
                "event_id": f"mock_gcal_{datetime.now().timestamp()}",
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "attendees": attendees or [],
                "description": description,
                "calendar_link": f"https://calendar.google.com/event/mock_{datetime.now().timestamp()}",
                "status": "created"
            }
        
        # In production, use Google Calendar API
        return {}
    
    def _get_mock_free_busy(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Generate mock free/busy times"""
        slots = []
        current = start_time
        
        while current < end_time:
            # Generate 3 available slots per day
            for hour in [9, 14, 16]:  # 9 AM, 2 PM, 4 PM
                slot_start = current.replace(hour=hour, minute=0, second=0, microsecond=0)
                slot_end = slot_start + timedelta(hours=1)
                
                if slot_start >= start_time and slot_end <= end_time:
                    slots.append({
                        "start": slot_start.isoformat(),
                        "end": slot_end.isoformat(),
                        "available": True,
                        "calendar_link": f"https://calendar.google.com/event/mock_{slot_start.timestamp()}"
                    })
            
            current += timedelta(days=1)
        
        return slots[:7]  # Return max 7 slots

class OutlookCalendarProvider(BaseProvider):
    """Outlook Calendar integration provider"""
    
    def test_connection(self) -> bool:
        if self.mock_mode:
            return True
        
        # In production, test Microsoft Graph API connection
        try:
            # This would use Microsoft Graph API to test connection
            return True
        except Exception:
            return False
    
    def get_status(self) -> str:
        if self.mock_mode:
            return "connected (mock)"
        return "connected" if self.test_connection() else "disconnected"
    
    def list_free_busy(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """List free/busy times"""
        if self.mock_mode:
            return self._get_mock_free_busy(start_time, end_time)
        
        # In production, use Microsoft Graph API
        return []
    
    def create_event(self, title: str, start_time: datetime, end_time: datetime, 
                    attendees: List[str] = None, description: str = None) -> Dict[str, Any]:
        """Create calendar event"""
        if self.mock_mode:
            return {
                "event_id": f"mock_outlook_{datetime.now().timestamp()}",
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "attendees": attendees or [],
                "description": description,
                "calendar_link": f"https://outlook.live.com/calendar/event/mock_{datetime.now().timestamp()}",
                "status": "created"
            }
        
        # In production, use Microsoft Graph API
        return {}
    
    def _get_mock_free_busy(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Generate mock free/busy times"""
        slots = []
        current = start_time
        
        while current < end_time:
            # Generate 2 available slots per day
            for hour in [10, 15]:  # 10 AM, 3 PM
                slot_start = current.replace(hour=hour, minute=0, second=0, microsecond=0)
                slot_end = slot_start + timedelta(hours=1)
                
                if slot_start >= start_time and slot_end <= end_time:
                    slots.append({
                        "start": slot_start.isoformat(),
                        "end": slot_end.isoformat(),
                        "available": True,
                        "calendar_link": f"https://outlook.live.com/calendar/event/mock_{slot_start.timestamp()}"
                    })
            
            current += timedelta(days=1)
        
        return slots[:5]  # Return max 5 slots

class CalendlyProvider(BaseProvider):
    """Calendly integration provider"""
    
    def __init__(self, auth_data: Dict[str, Any] = None):
        super().__init__(auth_data)
        self.calendly_link = auth_data.get("calendly_link", "") if auth_data else ""
    
    def test_connection(self) -> bool:
        if self.mock_mode:
            return bool(self.calendly_link)
        
        # In production, test Calendly API connection
        try:
            # This would use Calendly API to test connection
            return bool(self.calendly_link)
        except Exception:
            return False
    
    def get_status(self) -> str:
        if self.mock_mode:
            return "connected (mock)" if self.calendly_link else "disconnected"
        return "connected" if self.test_connection() else "disconnected"
    
    def get_available_times(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Get available Calendly times"""
        if self.mock_mode:
            return self._get_mock_calendly_times(start_time, end_time)
        
        # In production, use Calendly API
        return []
    
    def create_booking(self, event_type: str, start_time: datetime, 
                      prospect_email: str, prospect_name: str = None) -> Dict[str, Any]:
        """Create Calendly booking"""
        if self.mock_mode:
            return {
                "booking_id": f"mock_calendly_{datetime.now().timestamp()}",
                "event_type": event_type,
                "start_time": start_time.isoformat(),
                "prospect_email": prospect_email,
                "prospect_name": prospect_name,
                "booking_link": f"{self.calendly_link}/scheduled/{datetime.now().timestamp()}",
                "status": "confirmed"
            }
        
        # In production, use Calendly API
        return {}
    
    def _get_mock_calendly_times(self, start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Generate mock Calendly available times"""
        slots = []
        current = start_time
        
        while current < end_time:
            # Generate 2 available slots per day
            for hour in [11, 15]:  # 11 AM, 3 PM
                slot_start = current.replace(hour=hour, minute=0, second=0, microsecond=0)
                slot_end = slot_start + timedelta(minutes=30)
                
                if slot_start >= start_time and slot_end <= end_time:
                    slots.append({
                        "start": slot_start.isoformat(),
                        "end": slot_end.isoformat(),
                        "duration": 30,
                        "event_type": "30min_meeting",
                        "booking_link": f"{self.calendly_link}/scheduled/{slot_start.timestamp()}"
                    })
            
            current += timedelta(days=1)
        
        return slots[:6]  # Return max 6 slots
