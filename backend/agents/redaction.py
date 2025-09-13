"""
Redaction utilities for masking sensitive data in logs
"""

import re
from typing import Any, Dict, List

class RedactionUtils:
    # Email regex pattern
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    # Phone number patterns
    PHONE_PATTERNS = [
        re.compile(r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'),  # US format
        re.compile(r'\+?[0-9]{1,3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}'),  # International
    ]
    
    # Credit card pattern (basic)
    CREDIT_CARD_PATTERN = re.compile(r'\b[0-9]{4}[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}\b')
    
    # SSN pattern
    SSN_PATTERN = re.compile(r'\b[0-9]{3}[-.\s]?[0-9]{2}[-.\s]?[0-9]{4}\b')
    
    @classmethod
    def mask_email(cls, email: str) -> str:
        """Mask email address"""
        if not email or '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            masked_local = '*' * len(local)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        return f"{masked_local}@{domain}"
    
    @classmethod
    def mask_phone(cls, phone: str) -> str:
        """Mask phone number"""
        if not phone:
            return phone
        
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) < 4:
            return '*' * len(phone)
        
        # Keep first 3 and last 4 digits, mask the middle
        if len(digits) >= 10:
            return phone[:3] + '*' * (len(phone) - 7) + phone[-4:]
        else:
            return phone[:2] + '*' * (len(phone) - 4) + phone[-2:]
    
    @classmethod
    def mask_credit_card(cls, card: str) -> str:
        """Mask credit card number"""
        if not card:
            return card
        
        digits = re.sub(r'\D', '', card)
        if len(digits) < 8:
            return '*' * len(card)
        
        return card[:4] + '*' * (len(card) - 8) + card[-4:]
    
    @classmethod
    def mask_ssn(cls, ssn: str) -> str:
        """Mask SSN"""
        if not ssn:
            return ssn
        
        digits = re.sub(r'\D', '', ssn)
        if len(digits) != 9:
            return '*' * len(ssn)
        
        return ssn[:3] + '-' + '*' * 2 + '-' + ssn[-4:]
    
    @classmethod
    def redact_text(cls, text: str) -> str:
        """Redact sensitive information from text"""
        if not text:
            return text
        
        # Mask emails
        text = cls.EMAIL_PATTERN.sub(lambda m: cls.mask_email(m.group()), text)
        
        # Mask phone numbers
        for pattern in cls.PHONE_PATTERNS:
            text = pattern.sub(lambda m: cls.mask_phone(m.group()), text)
        
        # Mask credit cards
        text = cls.CREDIT_CARD_PATTERN.sub(lambda m: cls.mask_credit_card(m.group()), text)
        
        # Mask SSNs
        text = cls.SSN_PATTERN.sub(lambda m: cls.mask_ssn(m.group()), text)
        
        return text
    
    @classmethod
    def redact_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Redact sensitive information from dictionary"""
        if not isinstance(data, dict):
            return data
        
        redacted = {}
        for key, value in data.items():
            if isinstance(value, str):
                redacted[key] = cls.redact_text(value)
            elif isinstance(value, dict):
                redacted[key] = cls.redact_dict(value)
            elif isinstance(value, list):
                redacted[key] = [cls.redact_dict(item) if isinstance(item, dict) 
                               else cls.redact_text(item) if isinstance(item, str) 
                               else item for item in value]
            else:
                redacted[key] = value
        
        return redacted
    
    @classmethod
    def redact_log_data(cls, data: Any) -> Any:
        """Redact sensitive data for logging"""
        if isinstance(data, str):
            return cls.redact_text(data)
        elif isinstance(data, dict):
            return cls.redact_dict(data)
        elif isinstance(data, list):
            return [cls.redact_log_data(item) for item in data]
        else:
            return data
