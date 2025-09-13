"""
Integration providers for Inno Supps
"""

from .base import BaseProvider
from .email import GmailProvider, M365Provider
from .calendar import GoogleCalendarProvider, OutlookCalendarProvider, CalendlyProvider
from .crm import HubSpotProvider, SalesforceProvider
from .enrichment import ApolloProvider
from .chat import SlackProvider
from .telephony import TwilioProvider, ZoomProvider
from .transcription import OpenAIWhisperProvider

__all__ = [
    "BaseProvider",
    "GmailProvider",
    "M365Provider", 
    "GoogleCalendarProvider",
    "OutlookCalendarProvider",
    "CalendlyProvider",
    "HubSpotProvider",
    "SalesforceProvider",
    "ApolloProvider",
    "SlackProvider",
    "TwilioProvider",
    "ZoomProvider",
    "OpenAIWhisperProvider"
]
