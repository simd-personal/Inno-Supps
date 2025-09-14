"""
Email providers (Gmail, Microsoft 365)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .base import BaseProvider
from config import settings

class GmailProvider(BaseProvider):
    """Gmail integration provider"""
    
    def test_connection(self) -> bool:
        if self.mock_mode:
            return True
        
        # In production, test Gmail API connection
        try:
            # This would use Gmail API to test connection
            return True
        except Exception:
            return False
    
    def get_status(self) -> str:
        if self.mock_mode:
            return "connected (mock)"
        return "connected" if self.test_connection() else "disconnected"
    
    def list_threads(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """List email threads"""
        if self.mock_mode:
            return self._get_mock_threads(max_results)
        
        # In production, use Gmail API
        return []
    
    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get specific thread with messages"""
        if self.mock_mode:
            return self._get_mock_thread(thread_id)
        
        # In production, use Gmail API
        return {}
    
    def send_email(self, to: str, subject: str, body: str, thread_id: str = None) -> Dict[str, Any]:
        """Send email"""
        if self.mock_mode:
            return {
                "message_id": f"mock_{datetime.now().timestamp()}",
                "thread_id": thread_id or f"mock_thread_{datetime.now().timestamp()}",
                "status": "sent"
            }
        
        # In production, use Gmail API
        return {}
    
    def _get_mock_threads(self, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock email threads"""
        threads = []
        for i in range(min(max_results, 10)):
            threads.append({
                "id": f"mock_thread_{i}",
                "subject": f"Mock Email Thread {i}",
                "snippet": f"This is a mock email thread {i} for testing purposes.",
                "messages": [
                    {
                        "id": f"mock_message_{i}_1",
                        "from": f"sender{i}@example.com",
                        "to": "user@company.com",
                        "subject": f"Mock Email Thread {i}",
                        "body": f"This is the body of mock email {i}.",
                        "date": (datetime.now() - timedelta(days=i)).isoformat()
                    }
                ]
            })
        return threads
    
    def _get_mock_thread(self, thread_id: str) -> Dict[str, Any]:
        """Generate mock thread data"""
        return {
            "id": thread_id,
            "subject": f"Mock Thread: {thread_id}",
            "messages": [
                {
                    "id": f"{thread_id}_msg_1",
                    "from": "prospect@company.com",
                    "to": "user@company.com",
                    "subject": f"Mock Thread: {thread_id}",
                    "body": "This is a mock email body for testing purposes.",
                    "date": datetime.now().isoformat()
                }
            ]
        }

class M365Provider(BaseProvider):
    """Microsoft 365 integration provider"""
    
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
    
    def list_threads(self, max_results: int = 100) -> List[Dict[str, Any]]:
        """List email threads"""
        if self.mock_mode:
            return self._get_mock_threads(max_results)
        
        # In production, use Microsoft Graph API
        return []
    
    def get_thread(self, thread_id: str) -> Dict[str, Any]:
        """Get specific thread with messages"""
        if self.mock_mode:
            return self._get_mock_thread(thread_id)
        
        # In production, use Microsoft Graph API
        return {}
    
    def send_email(self, to: str, subject: str, body: str, thread_id: str = None) -> Dict[str, Any]:
        """Send email"""
        if self.mock_mode:
            return {
                "message_id": f"mock_m365_{datetime.now().timestamp()}",
                "thread_id": thread_id or f"mock_m365_thread_{datetime.now().timestamp()}",
                "status": "sent"
            }
        
        # In production, use Microsoft Graph API
        return {}
    
    def _get_mock_threads(self, max_results: int) -> List[Dict[str, Any]]:
        """Generate mock email threads"""
        threads = []
        for i in range(min(max_results, 10)):
            threads.append({
                "id": f"mock_m365_thread_{i}",
                "subject": f"Mock M365 Email Thread {i}",
                "snippet": f"This is a mock M365 email thread {i} for testing purposes.",
                "messages": [
                    {
                        "id": f"mock_m365_message_{i}_1",
                        "from": f"sender{i}@company.com",
                        "to": "user@company.com",
                        "subject": f"Mock M365 Email Thread {i}",
                        "body": f"This is the body of mock M365 email {i}.",
                        "date": (datetime.now() - timedelta(days=i)).isoformat()
                    }
                ]
            })
        return threads
    
    def _get_mock_thread(self, thread_id: str) -> Dict[str, Any]:
        """Generate mock thread data"""
        return {
            "id": thread_id,
            "subject": f"Mock M365 Thread: {thread_id}",
            "messages": [
                {
                    "id": f"{thread_id}_msg_1",
                    "from": "prospect@company.com",
                    "to": "user@company.com",
                    "subject": f"Mock M365 Thread: {thread_id}",
                    "body": "This is a mock M365 email body for testing purposes.",
                    "date": datetime.now().isoformat()
                }
            ]
        }
