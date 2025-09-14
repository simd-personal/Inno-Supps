"""
Base provider interface for integrations
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from config import settings

class BaseProvider(ABC):
    """Base class for all integration providers"""
    
    def __init__(self, auth_data: Dict[str, Any] = None):
        self.auth_data = auth_data or {}
        self.mock_mode = settings.mock_mode
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Test the connection to the provider"""
        pass
    
    @abstractmethod
    def get_status(self) -> str:
        """Get the current status of the provider"""
        pass
    
    def is_mock_mode(self) -> bool:
        """Check if provider is in mock mode"""
        return self.mock_mode
    
    def get_mock_data(self, data_type: str) -> Any:
        """Get mock data for testing"""
        return None
