"""
Agent tools implementation
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from backend.agents.tool_registry import tool_registry
from backend.services.llm_service import LLMService
from backend.config import settings

# Initialize LLM service
llm_service = LLMService()

@tool_registry.register
def classify_intent(email_text: str) -> Dict[str, Any]:
    """
    Classify the intent of an email to determine response type and urgency
    
    Args:
        email_text: The email content to classify
        
    Returns:
        Dictionary with reply_type, urgency, and book_meeting flags
    """
    if settings.mock_mode:
        # Mock response for testing
        return {
            "reply_type": "positive",
            "urgency": "medium",
            "book_meeting": True
        }
    
    try:
        prompt = f"""
        Analyze this email and classify its intent:
        
        Email: {email_text}
        
        Return a JSON response with:
        - reply_type: "positive", "negative", "neutral", or "question"
        - urgency: "low", "medium", or "high"
        - book_meeting: true if they want to schedule a meeting, false otherwise
        - sentiment: "positive", "negative", or "neutral"
        - key_topics: list of main topics mentioned
        """
        
        response = llm_service.generate_completion(prompt, temperature=0.1)
        
        # Try to parse JSON response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "reply_type": "neutral",
                "urgency": "medium", 
                "book_meeting": False,
                "sentiment": "neutral",
                "key_topics": []
            }
    
    except Exception as e:
        print(f"Error in classify_intent: {e}")
        return {
            "reply_type": "neutral",
            "urgency": "low",
            "book_meeting": False,
            "sentiment": "neutral",
            "key_topics": []
        }

@tool_registry.register
def draft_email(context: Dict[str, Any], style: str = "professional") -> Dict[str, str]:
    """
    Draft an email based on context and style
    
    Args:
        context: Dictionary with prospect info, campaign details, etc.
        style: Email style - "professional", "casual", "urgent", "follow_up"
        
    Returns:
        Dictionary with subject and body
    """
    if settings.mock_mode:
        return {
            "subject": f"Quick question about {context.get('company', 'your business')}",
            "body": f"Hi {context.get('name', 'there')},\n\nI hope this email finds you well. I wanted to reach out regarding {context.get('topic', 'a potential opportunity')}.\n\nBest regards,\n[Your Name]"
        }
    
    try:
        prompt = f"""
        Draft a {style} email with the following context:
        
        Context: {json.dumps(context, indent=2)}
        
        Return a JSON response with:
        - subject: Compelling subject line
        - body: Professional email body
        - tone: The tone used
        - call_to_action: The main CTA
        """
        
        response = llm_service.generate_completion(prompt, temperature=0.7)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "subject": f"Quick question about {context.get('company', 'your business')}",
                "body": f"Hi {context.get('name', 'there')},\n\nI hope this email finds you well.\n\nBest regards,\n[Your Name]",
                "tone": style,
                "call_to_action": "Schedule a call"
            }
    
    except Exception as e:
        print(f"Error in draft_email: {e}")
        return {
            "subject": f"Quick question about {context.get('company', 'your business')}",
            "body": f"Hi {context.get('name', 'there')},\n\nI hope this email finds you well.\n\nBest regards,\n[Your Name]",
            "tone": style,
            "call_to_action": "Schedule a call"
        }

@tool_registry.register
def calendar_find_slots(preferences: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Find available calendar slots based on preferences
    
    Args:
        preferences: Dictionary with date_range, duration, timezone, etc.
        
    Returns:
        List of available slots with start, end, and link
    """
    if settings.mock_mode:
        # Generate mock slots for the next 7 days
        from datetime import datetime, timedelta
        base_date = datetime.now()
        slots = []
        
        for i in range(3):  # 3 slots
            start_time = base_date + timedelta(days=i+1, hours=9)
            end_time = start_time + timedelta(hours=1)
            
            slots.append({
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "link": f"https://calendly.com/demo/{start_time.strftime('%Y%m%d%H%M')}"
            })
        
        return slots
    
    # In production, this would integrate with calendar providers
    # For now, return mock data
    return [
        {
            "start": "2024-01-16T09:00:00Z",
            "end": "2024-01-16T10:00:00Z", 
            "link": "https://calendly.com/demo/202401160900"
        },
        {
            "start": "2024-01-17T14:00:00Z",
            "end": "2024-01-17T15:00:00Z",
            "link": "https://calendly.com/demo/202401171400"
        }
    ]

@tool_registry.register
def calendar_book(prospect_email: str, slot: Dict[str, str]) -> Dict[str, Any]:
    """
    Book a calendar slot with a prospect
    
    Args:
        prospect_email: Email of the prospect
        slot: Slot details with start, end, link
        
    Returns:
        Dictionary with status and booking details
    """
    if settings.mock_mode:
        return {
            "status": "success",
            "booking_id": "mock_booking_123",
            "calendar_link": slot.get("link"),
            "confirmation": "Meeting booked successfully"
        }
    
    # In production, this would integrate with calendar providers
    return {
        "status": "success",
        "booking_id": "booking_123",
        "calendar_link": slot.get("link"),
        "confirmation": "Meeting booked successfully"
    }

@tool_registry.register
def fetch_company_profile(domain: str) -> Dict[str, Any]:
    """
    Fetch company profile information
    
    Args:
        domain: Company domain (e.g., "example.com")
        
    Returns:
        Dictionary with company information
    """
    if settings.mock_mode:
        return {
            "name": f"{domain.split('.')[0].title()} Inc.",
            "size": "50-200 employees",
            "industry": "Technology",
            "site": f"https://{domain}",
            "summary": f"Leading technology company in the {domain.split('.')[0]} space"
        }
    
    # In production, this would integrate with data enrichment APIs
    return {
        "name": f"{domain.split('.')[0].title()} Inc.",
        "size": "50-200 employees", 
        "industry": "Technology",
        "site": f"https://{domain}",
        "summary": f"Leading technology company in the {domain.split('.')[0]} space"
    }

@tool_registry.register
def enrich_person(name: str, company: str) -> Dict[str, Any]:
    """
    Enrich person information
    
    Args:
        name: Person's name
        company: Company name
        
    Returns:
        Dictionary with enriched person data
    """
    if settings.mock_mode:
        return {
            "title": "Senior Manager",
            "email_guess": f"{name.lower().replace(' ', '.')}@{company.lower().replace(' ', '')}.com",
            "linkedin": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
            "summary": f"Experienced professional at {company}"
        }
    
    # In production, this would integrate with data enrichment APIs
    return {
        "title": "Senior Manager",
        "email_guess": f"{name.lower().replace(' ', '.')}@{company.lower().replace(' ', '')}.com",
        "linkedin": f"https://linkedin.com/in/{name.lower().replace(' ', '-')}",
        "summary": f"Experienced professional at {company}"
    }

@tool_registry.register
def analyze_transcript(transcript_text: str) -> Dict[str, List[str]]:
    """
    Analyze call transcript for insights
    
    Args:
        transcript_text: The call transcript
        
    Returns:
        Dictionary with highlights, objections, actions, and coaching points
    """
    if settings.mock_mode:
        return {
            "highlights": [
                "Prospect showed interest in pricing",
                "Mentioned budget constraints",
                "Wants to see a demo"
            ],
            "objections": [
                "Price is too high",
                "Need to check with team"
            ],
            "actions": [
                "Send pricing information",
                "Schedule demo call",
                "Follow up in 1 week"
            ],
            "coaching": [
                "Address price objection with value proposition",
                "Ask about decision-making process"
            ]
        }
    
    try:
        prompt = f"""
        Analyze this call transcript and extract key insights:
        
        Transcript: {transcript_text}
        
        Return a JSON response with:
        - highlights: List of key points mentioned
        - objections: List of objections raised
        - actions: List of next steps/actions
        - coaching: List of coaching recommendations
        """
        
        response = llm_service.generate_completion(prompt, temperature=0.3)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "highlights": [],
                "objections": [],
                "actions": [],
                "coaching": []
            }
    
    except Exception as e:
        print(f"Error in analyze_transcript: {e}")
        return {
            "highlights": [],
            "objections": [],
            "actions": [],
            "coaching": []
        }

@tool_registry.register
def generate_niche_report(keywords: List[str], region: str = "US", size_range: str = "1-50") -> str:
    """
    Generate a comprehensive niche market report
    
    Args:
        keywords: List of keywords related to the niche
        region: Geographic region to analyze
        size_range: Company size range (e.g., "1-50", "51-200", "201-1000")
        
    Returns:
        Markdown report with market analysis
    """
    if settings.mock_mode:
        return f"""
# Niche Market Report: {', '.join(keywords)}

## Executive Summary
This report analyzes the market opportunity for {', '.join(keywords)} in the {region} region, focusing on companies with {size_range} employees.

## Market Size
- Total Addressable Market: $2.8B
- Serviceable Addressable Market: $450M
- Serviceable Obtainable Market: $45M

## Key Insights
1. High growth potential in this niche
2. Limited competition in the {size_range} segment
3. Strong demand for automation solutions

## Recommendations
- Focus on {keywords[0]} as primary offering
- Target companies in {region} with {size_range} employees
- Develop partnerships with key industry players
        """
    
    try:
        prompt = f"""
        Generate a comprehensive niche market report for:
        - Keywords: {', '.join(keywords)}
        - Region: {region}
        - Company Size: {size_range} employees
        
        Include:
        1. Executive Summary
        2. Market Size and Growth
        3. Competitive Landscape
        4. Target Customer Analysis
        5. Revenue Opportunities
        6. Implementation Strategy
        7. Risk Assessment
        
        Format as detailed markdown report.
        """
        
        response = llm_service.generate_completion(prompt, temperature=0.5)
        return response
    
    except Exception as e:
        print(f"Error in generate_niche_report: {e}")
        return f"# Niche Report: {', '.join(keywords)}\n\nError generating report: {e}"

@tool_registry.register
def generate_growth_plan(inputs_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a comprehensive growth plan
    
    Args:
        inputs_json: Dictionary with business inputs (revenue, team size, goals, etc.)
        
    Returns:
        Dictionary with plan_md and kpis_json
    """
    if settings.mock_mode:
        return {
            "plan_md": f"""
# Growth Plan for {inputs_json.get('company_name', 'Your Company')}

## Current State
- Revenue: ${inputs_json.get('current_revenue', 0):,}
- Team Size: {inputs_json.get('team_size', 0)} employees
- Growth Rate: {inputs_json.get('growth_rate', 0)}%

## 12-Month Goals
- Target Revenue: ${inputs_json.get('target_revenue', 0):,}
- Target Team Size: {inputs_json.get('target_team_size', 0)} employees
- Target Growth Rate: {inputs_json.get('target_growth_rate', 0)}%

## Key Strategies
1. **Sales & Marketing**: Implement automated lead generation
2. **Product Development**: Focus on customer feedback integration
3. **Operations**: Streamline processes and improve efficiency
4. **Team Building**: Hire key roles and develop existing talent

## Next Steps
1. Implement CRM system
2. Launch marketing campaigns
3. Optimize sales process
4. Scale team strategically
            """,
            "kpis_json": {
                "monthly_revenue": inputs_json.get('target_revenue', 0) / 12,
                "customer_acquisition_cost": 150,
                "lifetime_value": 5000,
                "churn_rate": 0.05,
                "growth_rate": inputs_json.get('target_growth_rate', 0)
            }
        }
    
    try:
        prompt = f"""
        Generate a comprehensive 12-month growth plan based on these inputs:
        
        {json.dumps(inputs_json, indent=2)}
        
        Return a JSON response with:
        - plan_md: Detailed markdown growth plan
        - kpis_json: Key performance indicators and targets
        
        The plan should include:
        1. Current state analysis
        2. 12-month goals and objectives
        3. Key strategies and initiatives
        4. Resource requirements
        5. Risk mitigation
        6. Success metrics and KPIs
        """
        
        response = llm_service.generate_completion(prompt, temperature=0.6)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "plan_md": f"# Growth Plan\n\nError generating plan: Invalid response format",
                "kpis_json": {}
            }
    
    except Exception as e:
        print(f"Error in generate_growth_plan: {e}")
        return {
            "plan_md": f"# Growth Plan\n\nError generating plan: {e}",
            "kpis_json": {}
        }
