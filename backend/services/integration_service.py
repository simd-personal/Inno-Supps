"""
Integration service for managing all providers
"""

from typing import Dict, Any, List, Optional, Type
from database import Integration, IntegrationType, get_db
from providers import (
    GmailProvider, M365Provider,
    GoogleCalendarProvider, OutlookCalendarProvider, CalendlyProvider,
    HubSpotProvider, SalesforceProvider,
    ApolloProvider,
    SlackProvider,
    TwilioProvider, ZoomProvider,
    OpenAIWhisperProvider
)
from sqlalchemy.orm import Session

class IntegrationService:
    """Service for managing integration providers"""
    
    def __init__(self):
        self.providers = {
            IntegrationType.EMAIL_GMAIL: GmailProvider,
            IntegrationType.EMAIL_M365: M365Provider,
            IntegrationType.CALENDAR_GCAL: GoogleCalendarProvider,
            IntegrationType.CALENDAR_OUTLOOK: OutlookCalendarProvider,
            IntegrationType.CALENDLY: CalendlyProvider,
            IntegrationType.HUBSPOT: HubSpotProvider,
            IntegrationType.SALESFORCE: SalesforceProvider,
            IntegrationType.APOLLO: ApolloProvider,
            IntegrationType.SLACK: SlackProvider,
            IntegrationType.TWILIO: TwilioProvider,
            IntegrationType.ZOOM: ZoomProvider,
        }
    
    def get_provider(self, integration_type: IntegrationType, auth_data: Dict[str, Any] = None) -> Any:
        """Get provider instance for integration type"""
        provider_class = self.providers.get(integration_type)
        if not provider_class:
            raise ValueError(f"Unknown integration type: {integration_type}")
        
        return provider_class(auth_data)
    
    def test_integration(self, workspace_id: str, integration_id: str) -> Dict[str, Any]:
        """Test integration connection"""
        db = next(get_db())
        try:
            integration = db.query(Integration).filter(
                Integration.workspace_id == workspace_id,
                Integration.id == integration_id
            ).first()
            
            if not integration:
                return {"status": "error", "message": "Integration not found"}
            
            provider = self.get_provider(integration.type, integration.auth_json)
            is_connected = provider.test_connection()
            
            # Update integration status
            integration.status = "connected" if is_connected else "disconnected"
            db.commit()
            
            return {
                "status": "success" if is_connected else "error",
                "connected": is_connected,
                "provider_status": provider.get_status()
            }
        finally:
            db.close()
    
    def get_integration_status(self, workspace_id: str) -> Dict[str, Any]:
        """Get status of all integrations for workspace"""
        db = next(get_db())
        try:
            integrations = db.query(Integration).filter(
                Integration.workspace_id == workspace_id
            ).all()
            
            status = {}
            for integration in integrations:
                provider = self.get_provider(integration.type, integration.auth_json)
                status[integration.type.value] = {
                    "id": str(integration.id),
                    "status": integration.status,
                    "provider_status": provider.get_status(),
                    "connected": provider.test_connection()
                }
            
            return status
        finally:
            db.close()
    
    def create_integration(self, workspace_id: str, integration_type: IntegrationType, 
                          auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new integration"""
        db = next(get_db())
        try:
            # Test connection first
            provider = self.get_provider(integration_type, auth_data)
            is_connected = provider.test_connection()
            
            # Create integration record
            integration = Integration(
                workspace_id=workspace_id,
                type=integration_type,
                status="connected" if is_connected else "disconnected",
                auth_json=auth_data
            )
            db.add(integration)
            db.commit()
            db.refresh(integration)
            
            return {
                "status": "success",
                "integration_id": str(integration.id),
                "connected": is_connected,
                "provider_status": provider.get_status()
            }
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def update_integration(self, workspace_id: str, integration_id: str, 
                          auth_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update integration auth data"""
        db = next(get_db())
        try:
            integration = db.query(Integration).filter(
                Integration.workspace_id == workspace_id,
                Integration.id == integration_id
            ).first()
            
            if not integration:
                return {"status": "error", "message": "Integration not found"}
            
            # Test connection with new auth data
            provider = self.get_provider(integration.type, auth_data)
            is_connected = provider.test_connection()
            
            # Update integration
            integration.auth_json = auth_data
            integration.status = "connected" if is_connected else "disconnected"
            db.commit()
            
            return {
                "status": "success",
                "connected": is_connected,
                "provider_status": provider.get_status()
            }
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def delete_integration(self, workspace_id: str, integration_id: str) -> Dict[str, Any]:
        """Delete integration"""
        db = next(get_db())
        try:
            integration = db.query(Integration).filter(
                Integration.workspace_id == workspace_id,
                Integration.id == integration_id
            ).first()
            
            if not integration:
                return {"status": "error", "message": "Integration not found"}
            
            db.delete(integration)
            db.commit()
            
            return {"status": "success", "message": "Integration deleted"}
        except Exception as e:
            db.rollback()
            return {"status": "error", "message": str(e)}
        finally:
            db.close()
    
    def get_available_integrations(self) -> List[Dict[str, Any]]:
        """Get list of available integration types"""
        return [
            {
                "type": "email_gmail",
                "name": "Gmail",
                "description": "Connect Gmail for email management",
                "icon": "gmail",
                "category": "email"
            },
            {
                "type": "email_m365",
                "name": "Microsoft 365",
                "description": "Connect Microsoft 365 for email management",
                "icon": "microsoft",
                "category": "email"
            },
            {
                "type": "calendar_gcal",
                "name": "Google Calendar",
                "description": "Connect Google Calendar for scheduling",
                "icon": "google",
                "category": "calendar"
            },
            {
                "type": "calendar_outlook",
                "name": "Outlook Calendar",
                "description": "Connect Outlook Calendar for scheduling",
                "icon": "microsoft",
                "category": "calendar"
            },
            {
                "type": "calendly",
                "name": "Calendly",
                "description": "Connect Calendly for automated scheduling",
                "icon": "calendly",
                "category": "calendar"
            },
            {
                "type": "hubspot",
                "name": "HubSpot",
                "description": "Connect HubSpot for CRM management",
                "icon": "hubspot",
                "category": "crm"
            },
            {
                "type": "salesforce",
                "name": "Salesforce",
                "description": "Connect Salesforce for CRM management",
                "icon": "salesforce",
                "category": "crm"
            },
            {
                "type": "apollo",
                "name": "Apollo",
                "description": "Connect Apollo for data enrichment",
                "icon": "apollo",
                "category": "enrichment"
            },
            {
                "type": "slack",
                "name": "Slack",
                "description": "Connect Slack for team communication",
                "icon": "slack",
                "category": "chat"
            },
            {
                "type": "twilio",
                "name": "Twilio",
                "description": "Connect Twilio for phone calls and SMS",
                "icon": "twilio",
                "category": "telephony"
            },
            {
                "type": "zoom",
                "name": "Zoom",
                "description": "Connect Zoom for video meetings",
                "icon": "zoom",
                "category": "telephony"
            }
        ]

# Global integration service instance
integration_service = IntegrationService()
