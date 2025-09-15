"""
AI Agents routes for Inno Supps
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests
import openai
import os

router = APIRouter(prefix="/api/agents", tags=["ai-agents"])

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Request/Response models
class ColdEmailRequest(BaseModel):
    prospect_name: str
    company: str
    role: str
    pain_points: List[str]
    value_proposition: str
    email_type: Optional[str] = "cold_outreach"

class NicheResearchRequest(BaseModel):
    skills: List[str]
    interests: List[str]
    budget: int
    experience_level: str
    time_commitment: Optional[str] = "part_time"

class ColdEmailResponse(BaseModel):
    subject: str
    email_body: str
    personalization_score: int
    call_to_action: str
    follow_up_suggestions: List[str]

class EmailSequenceRequest(BaseModel):
    prospect_name: str
    company: str
    role: str
    pain_points: List[str]
    value_proposition: str
    sequence_length: Optional[int] = 5
    industry: Optional[str] = None

class EmailSequenceResponse(BaseModel):
    sequence: List[Dict[str, Any]]
    total_emails: int
    estimated_duration_days: int
    success_metrics: Dict[str, Any]

class EmailTemplateRequest(BaseModel):
    name: str
    category: str
    subject_template: str
    body_template: str
    variables: List[str]
    industry: Optional[str] = None
    use_case: Optional[str] = None

class EmailTemplateResponse(BaseModel):
    id: str
    name: str
    category: str
    subject_template: str
    body_template: str
    variables: List[str]
    industry: Optional[str]
    use_case: Optional[str]
    success_rate: Optional[float]
    usage_count: int

class ABTestRequest(BaseModel):
    name: str
    description: str
    base_email_id: str
    variants: List[Dict[str, Any]]
    test_duration_days: int
    success_metric: str  # open_rate, reply_rate, meeting_rate

class ABTestResponse(BaseModel):
    test_id: str
    name: str
    description: str
    base_email_id: str
    variants: List[Dict[str, Any]]
    test_duration_days: int
    success_metric: str
    status: str  # active, completed, paused
    results: Optional[Dict[str, Any]] = None

class NicheResearchResponse(BaseModel):
    recommended_niches: List[Dict[str, Any]]
    market_analysis: Dict[str, Any]
    implementation_strategy: List[str]
    risk_assessment: Dict[str, Any]

async def clean_and_improve_input(request: ColdEmailRequest) -> Dict[str, Any]:
    """Clean and improve user input using GPT before generating email"""
    try:
        # Create a prompt to clean and improve the input
        prompt = f"""
        Please clean and improve the following prospect information for a professional cold email:
        
        Original Input:
        - Name: {request.prospect_name}
        - Company: {request.company}
        - Role: {request.role}
        - Pain Points: {', '.join(request.pain_points)}
        - Value Proposition: {request.value_proposition}
        
        Please provide cleaned and improved versions that:
        1. Fix any spelling, grammar, or formatting errors
        2. Make the language more professional and clear
        3. Ensure proper capitalization and punctuation
        4. Improve the value proposition to be more compelling
        5. Make pain points more specific and actionable
        6. Ensure the role is properly formatted (e.g., "VP of Marketing" not "vp marketing")
        
        Return the response in this exact JSON format:
        {{
            "prospect_name": "cleaned name",
            "company": "cleaned company name",
            "role": "cleaned role title",
            "pain_points": ["cleaned pain point 1", "cleaned pain point 2"],
            "value_proposition": "improved value proposition"
        }}
        """
        
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional business communication expert. Clean and improve user input for cold email generation."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        # Parse the cleaned response
        cleaned_text = response.choices[0].message.content.strip()
        
        # Extract JSON from the response
        import json
        import re
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            cleaned_data = json.loads(json_match.group())
            return cleaned_data
        else:
            # Fallback if JSON parsing fails
            return {
                "prospect_name": request.prospect_name.title(),
                "company": request.company.title(),
                "role": request.role.title(),
                "pain_points": [point.strip().title() for point in request.pain_points],
                "value_proposition": request.value_proposition
            }
            
    except Exception as e:
        print(f"Error cleaning input: {e}")
        # Fallback to basic cleaning
        return {
            "prospect_name": request.prospect_name.title(),
            "company": request.company.title(),
            "role": request.role.title(),
            "pain_points": [point.strip().title() for point in request.pain_points],
            "value_proposition": request.value_proposition
        }

async def clean_and_improve_niche_input(request: NicheResearchRequest) -> Dict[str, Any]:
    """Clean and improve niche research input using GPT"""
    try:
        # Create a prompt to clean and improve the niche research input
        prompt = f"""
        Please clean and improve the following niche research information:
        
        Original Input:
        - Skills: {', '.join(request.skills)}
        - Interests: {', '.join(request.interests)}
        - Experience Level: {request.experience_level}
        
        Please provide cleaned and improved versions that:
        1. Fix any spelling, grammar, or formatting errors
        2. Make the language more professional and clear
        3. Ensure proper capitalization and punctuation
        4. Make skills more specific and actionable
        5. Make interests more focused and business-relevant
        6. Standardize experience level (e.g., "Beginner", "Intermediate", "Advanced")
        
        Return the response in this exact JSON format:
        {{
            "skills": ["cleaned skill 1", "cleaned skill 2"],
            "interests": ["cleaned interest 1", "cleaned interest 2"],
            "experience_level": "cleaned experience level"
        }}
        """
        
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional business consultant. Clean and improve user input for niche research analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.3
        )
        
        # Parse the cleaned response
        cleaned_text = response.choices[0].message.content.strip()
        
        # Extract JSON from the response
        import json
        import re
        
        # Find JSON in the response
        json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
        if json_match:
            cleaned_data = json.loads(json_match.group())
            return cleaned_data
        else:
            # Fallback if JSON parsing fails
            return {
                "skills": [skill.strip().title() for skill in request.skills],
                "interests": [interest.strip().title() for interest in request.interests],
                "experience_level": request.experience_level.title()
            }
            
    except Exception as e:
        print(f"Error cleaning niche input: {e}")
        # Fallback to basic cleaning
        return {
            "skills": [skill.strip().title() for skill in request.skills],
            "interests": [interest.strip().title() for interest in request.interests],
            "experience_level": request.experience_level.title()
        }

@router.post("/cold-email-writer/generate", response_model=ColdEmailResponse)
async def generate_cold_email(request: ColdEmailRequest):
    """Generate a personalized cold email"""
    try:
        # First, clean and improve the user input using GPT
        cleaned_input = await clean_and_improve_input(request)
        
        # Call the simple AI API with cleaned input
        ai_response = requests.post(
            "http://localhost:8001/generate_cold_email",
            json={
                "prospect_name": cleaned_input["prospect_name"],
                "company": cleaned_input["company"],
                "role": cleaned_input["role"],
                "pain_points": cleaned_input["pain_points"],
                "value_proposition": cleaned_input["value_proposition"],
                "email_type": request.email_type
            },
            timeout=30
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            return ColdEmailResponse(
                subject=data.get("subject", "Let's discuss how we can help"),
                email_body=data.get("email_body", "Email generation failed"),
                personalization_score=data.get("personalization_score", 85),
                call_to_action=data.get("call_to_action", "Schedule a call"),
                follow_up_suggestions=data.get("follow_up_suggestions", ["Follow up in 3 days", "Send case study"])
            )
        else:
            raise HTTPException(status_code=500, detail="AI service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to mock data if AI service is down, using cleaned input
        cleaned_input = await clean_and_improve_input(request)
        return ColdEmailResponse(
            subject=f"Quick question about {cleaned_input['company']}'s growth strategy",
            email_body=f"""Hi {cleaned_input['prospect_name']},

I noticed {cleaned_input['company']} is facing some {', '.join(cleaned_input['pain_points'][:2])} challenges. 

As a {cleaned_input['role']}, you're probably looking for ways to {cleaned_input['value_proposition']}.

I've helped similar companies in your space achieve 40% faster growth through our proven methodology.

Would you be open to a 15-minute call this week to discuss how we might help {cleaned_input['company']}?

Best regards,
[Your Name]""",
            personalization_score=75,
            call_to_action="Schedule a 15-minute call",
            follow_up_suggestions=["Follow up in 3 days", "Send case study", "Connect on LinkedIn"]
        )

@router.post("/cold-email-writer/sequence", response_model=EmailSequenceResponse)
async def generate_email_sequence(request: EmailSequenceRequest):
    """Generate a complete email follow-up sequence"""
    try:
        # First, clean and improve the user input
        cleaned_input = await clean_and_improve_input(ColdEmailRequest(
            prospect_name=request.prospect_name,
            company=request.company,
            role=request.role,
            pain_points=request.pain_points,
            value_proposition=request.value_proposition
        ))
        
        # Call the AI service for sequence generation with cleaned input
        ai_response = requests.post(
            "http://localhost:8001/generate_email_sequence",
            json={
                "prospect_name": cleaned_input["prospect_name"],
                "company": cleaned_input["company"],
                "role": cleaned_input["role"],
                "pain_points": cleaned_input["pain_points"],
                "value_proposition": cleaned_input["value_proposition"],
                "sequence_length": request.sequence_length,
                "industry": request.industry
            },
            timeout=30
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            return EmailSequenceResponse(
                sequence=data.get("sequence", []),
                total_emails=data.get("total_emails", request.sequence_length),
                estimated_duration_days=data.get("estimated_duration_days", 14),
                success_metrics=data.get("success_metrics", {})
            )
        else:
            raise HTTPException(status_code=500, detail="AI service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to mock data if AI service is down, using cleaned input
        sequence = generate_mock_email_sequence(request, cleaned_input)
        return EmailSequenceResponse(
            sequence=sequence,
            total_emails=len(sequence),
            estimated_duration_days=14,
            success_metrics={
                "expected_open_rate": "25-35%",
                "expected_reply_rate": "8-12%",
                "expected_meeting_rate": "2-5%"
            }
        )

def generate_mock_email_sequence(request: EmailSequenceRequest, cleaned_input: Dict[str, Any] = None):
    """Generate a mock email sequence for fallback"""
    sequence = []
    
    # Use cleaned input if available, otherwise fall back to original
    if cleaned_input:
        prospect_name = cleaned_input["prospect_name"]
        company = cleaned_input["company"]
        role = cleaned_input["role"]
        pain_points = cleaned_input["pain_points"]
        value_proposition = cleaned_input["value_proposition"]
    else:
        prospect_name = request.prospect_name
        company = request.company
        role = request.role
        pain_points = request.pain_points
        value_proposition = request.value_proposition
    
    # Email 1: Initial outreach
    sequence.append({
        "step": 1,
        "day": 0,
        "subject": f"Quick question about {company}'s growth strategy",
        "email_body": f"""Hi {prospect_name},

I noticed {company} is facing some {', '.join(pain_points[:2])} challenges.

As a {role}, you're probably looking for ways to {value_proposition}.

I've helped similar companies in your space achieve 40% faster growth through our proven methodology.

Would you be open to a 15-minute call this week to discuss how we might help {company}?

Best regards,
[Your Name]""",
        "personalization_score": 85,
        "call_to_action": "Schedule a 15-minute call",
        "wait_days": 3
    })
    
    # Email 2: Value proposition
    sequence.append({
        "step": 2,
        "day": 3,
        "subject": f"Case study: How we helped {company}'s competitor scale",
        "email_body": f"""Hi {prospect_name},

Following up on my previous email about {company}'s growth challenges.

I thought you'd find this case study interesting - we recently helped [Competitor Company] in your industry achieve:
• 40% increase in lead generation
• 25% improvement in conversion rates
• $2M additional revenue in 6 months

The key was implementing our {value_proposition} approach.

Would you be interested in a brief 10-minute call to discuss how this could apply to {company}?

Best regards,
[Your Name]""",
        "personalization_score": 78,
        "call_to_action": "Schedule a 10-minute call",
        "wait_days": 4
    })
    
    # Email 3: Social proof
    sequence.append({
        "step": 3,
        "day": 7,
        "subject": f"Industry insights for {company}",
        "email_body": f"""Hi {prospect_name},

I understand you're busy, but I wanted to share some industry insights that might be valuable for {company}.

Based on our work with 50+ companies in your space, the top 3 challenges we see are:
1. {pain_points[0] if pain_points else 'Scaling efficiently'}
2. {pain_points[1] if len(pain_points) > 1 else 'Cost optimization'}
3. {pain_points[2] if len(pain_points) > 2 else 'Team productivity'}

We've developed a framework that addresses these specific issues. Would you be open to a quick 15-minute call to discuss?

Best regards,
[Your Name]""",
        "personalization_score": 72,
        "call_to_action": "Schedule a 15-minute call",
        "wait_days": 5
    })
    
    # Email 4: Urgency/Scarcity
    sequence.append({
        "step": 4,
        "day": 12,
        "subject": f"Last attempt - {company} growth opportunity",
        "email_body": f"""Hi {prospect_name},

I don't want to keep bothering you, but I believe there's a real opportunity for {company} to address {', '.join(pain_points[:2])}.

Our clients typically see results within 30 days of implementation. The window for Q1 impact is closing soon.

If you're interested in learning more, I'd be happy to share a 5-minute overview of our approach.

If not, I'll remove you from future communications.

Best regards,
[Your Name]""",
        "personalization_score": 65,
        "call_to_action": "5-minute overview or unsubscribe",
        "wait_days": 3
    })
    
    # Email 5: Final follow-up
    sequence.append({
        "step": 5,
        "day": 15,
        "subject": f"Final follow-up - {company}",
        "email_body": f"""Hi {prospect_name},

This is my final follow-up regarding {company}'s growth opportunities.

I understand if the timing isn't right, but I wanted to leave you with one valuable insight:

Companies that address {pain_points[0] if pain_points else 'their scaling challenges'} early typically see 3x better results than those who wait.

If you'd like to discuss this further in the future, feel free to reach out.

Best regards,
[Your Name]""",
        "personalization_score": 60,
        "call_to_action": "Future discussion",
        "wait_days": 0
    })
    
    return sequence

# Email Templates Library
@router.get("/email-templates", response_model=List[EmailTemplateResponse])
async def get_email_templates(category: Optional[str] = None, industry: Optional[str] = None):
    """Get all email templates, optionally filtered by category or industry"""
    templates = get_mock_email_templates()
    
    if category:
        templates = [t for t in templates if t["category"].lower() == category.lower()]
    if industry:
        templates = [t for t in templates if t["industry"] and t["industry"].lower() == industry.lower()]
    
    return templates

@router.post("/email-templates", response_model=EmailTemplateResponse)
async def create_email_template(request: EmailTemplateRequest):
    """Create a new email template"""
    template_id = f"template_{len(get_mock_email_templates()) + 1}"
    
    return EmailTemplateResponse(
        id=template_id,
        name=request.name,
        category=request.category,
        subject_template=request.subject_template,
        body_template=request.body_template,
        variables=request.variables,
        industry=request.industry,
        use_case=request.use_case,
        success_rate=None,
        usage_count=0
    )

@router.get("/email-templates/{template_id}", response_model=EmailTemplateResponse)
async def get_email_template(template_id: str):
    """Get a specific email template by ID"""
    templates = get_mock_email_templates()
    template = next((t for t in templates if t["id"] == template_id), None)
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template

def get_mock_email_templates():
    """Get mock email templates for demonstration"""
    return [
        {
            "id": "template_1",
            "name": "Cold Outreach - SaaS",
            "category": "cold_outreach",
            "subject_template": "Quick question about {company}'s {pain_point}",
            "body_template": """Hi {prospect_name},

I noticed {company} is facing some {pain_point} challenges.

As a {role}, you're probably looking for ways to {value_proposition}.

I've helped similar companies in your space achieve 40% faster growth through our proven methodology.

Would you be open to a 15-minute call this week to discuss how we might help {company}?

Best regards,
[Your Name]""",
            "variables": ["prospect_name", "company", "pain_point", "role", "value_proposition"],
            "industry": "SaaS",
            "use_case": "initial_outreach",
            "success_rate": 0.28,
            "usage_count": 150
        },
        {
            "id": "template_2",
            "name": "Follow-up - Value Proposition",
            "category": "follow_up",
            "subject_template": "Case study: How we helped {company}'s competitor scale",
            "body_template": """Hi {prospect_name},

Following up on my previous email about {company}'s growth challenges.

I thought you'd find this case study interesting - we recently helped [Competitor Company] in your industry achieve:
• 40% increase in lead generation
• 25% improvement in conversion rates
• $2M additional revenue in 6 months

The key was implementing our {value_proposition} approach.

Would you be interested in a brief 10-minute call to discuss how this could apply to {company}?

Best regards,
[Your Name]""",
            "variables": ["prospect_name", "company", "value_proposition"],
            "industry": "SaaS",
            "use_case": "value_proposition",
            "success_rate": 0.22,
            "usage_count": 89
        },
        {
            "id": "template_3",
            "name": "Social Proof - Industry Insights",
            "category": "social_proof",
            "subject_template": "Industry insights for {company}",
            "body_template": """Hi {prospect_name},

I understand you're busy, but I wanted to share some industry insights that might be valuable for {company}.

Based on our work with 50+ companies in your space, the top 3 challenges we see are:
1. {pain_point_1}
2. {pain_point_2}
3. {pain_point_3}

We've developed a framework that addresses these specific issues. Would you be open to a quick 15-minute call to discuss?

Best regards,
[Your Name]""",
            "variables": ["prospect_name", "company", "pain_point_1", "pain_point_2", "pain_point_3"],
            "industry": "SaaS",
            "use_case": "industry_insights",
            "success_rate": 0.19,
            "usage_count": 67
        },
        {
            "id": "template_4",
            "name": "Urgency - Last Attempt",
            "category": "urgency",
            "subject_template": "Last attempt - {company} growth opportunity",
            "body_template": """Hi {prospect_name},

I don't want to keep bothering you, but I believe there's a real opportunity for {company} to address {pain_points}.

Our clients typically see results within 30 days of implementation. The window for Q1 impact is closing soon.

If you're interested in learning more, I'd be happy to share a 5-minute overview of our approach.

If not, I'll remove you from future communications.

Best regards,
[Your Name]""",
            "variables": ["prospect_name", "company", "pain_points"],
            "industry": "SaaS",
            "use_case": "urgency",
            "success_rate": 0.15,
            "usage_count": 45
        },
        {
            "id": "template_5",
            "name": "E-commerce - Product Launch",
            "category": "cold_outreach",
            "subject_template": "New product launch for {company}",
            "body_template": """Hi {prospect_name},

I saw that {company} recently launched {product_name}. Congratulations!

I work with e-commerce companies to help them scale their marketing efforts and increase conversions.

Our clients typically see:
• 35% increase in conversion rates
• 50% improvement in customer lifetime value
• 60% reduction in customer acquisition costs

Would you be interested in a brief call to discuss how we might help {company} scale even further?

Best regards,
[Your Name]""",
            "variables": ["prospect_name", "company", "product_name"],
            "industry": "E-commerce",
            "use_case": "product_launch",
            "success_rate": 0.31,
            "usage_count": 23
        }
    ]

# A/B Testing for Email Variants
@router.post("/ab-tests", response_model=ABTestResponse)
async def create_ab_test(request: ABTestRequest):
    """Create a new A/B test for email variants"""
    test_id = f"ab_test_{len(get_mock_ab_tests()) + 1}"
    
    return ABTestResponse(
        test_id=test_id,
        name=request.name,
        description=request.description,
        base_email_id=request.base_email_id,
        variants=request.variants,
        test_duration_days=request.test_duration_days,
        success_metric=request.success_metric,
        status="active",
        results=None
    )

@router.get("/ab-tests", response_model=List[ABTestResponse])
async def get_ab_tests(status: Optional[str] = None):
    """Get all A/B tests, optionally filtered by status"""
    tests = get_mock_ab_tests()
    
    if status:
        tests = [t for t in tests if t["status"].lower() == status.lower()]
    
    return tests

@router.get("/ab-tests/{test_id}", response_model=ABTestResponse)
async def get_ab_test(test_id: str):
    """Get a specific A/B test by ID"""
    tests = get_mock_ab_tests()
    test = next((t for t in tests if t["test_id"] == test_id), None)
    
    if not test:
        raise HTTPException(status_code=404, detail="A/B test not found")
    
    return test

@router.post("/ab-tests/{test_id}/results", response_model=ABTestResponse)
async def update_ab_test_results(test_id: str, results: Dict[str, Any]):
    """Update A/B test results"""
    tests = get_mock_ab_tests()
    test = next((t for t in tests if t["test_id"] == test_id), None)
    
    if not test:
        raise HTTPException(status_code=404, detail="A/B test not found")
    
    test["results"] = results
    test["status"] = "completed"
    
    return test

def get_mock_ab_tests():
    """Get mock A/B tests for demonstration"""
    return [
        {
            "test_id": "ab_test_1",
            "name": "Subject Line Test - SaaS Outreach",
            "description": "Testing different subject lines for cold outreach emails",
            "base_email_id": "template_1",
            "variants": [
                {
                    "variant_id": "A",
                    "name": "Question-based Subject",
                    "subject": "Quick question about {company}'s {pain_point}",
                    "traffic_percentage": 50
                },
                {
                    "variant_id": "B", 
                    "name": "Value-based Subject",
                    "subject": "How {company} can increase revenue by 40%",
                    "traffic_percentage": 50
                }
            ],
            "test_duration_days": 7,
            "success_metric": "open_rate",
            "status": "completed",
            "results": {
                "variant_a": {
                    "opens": 150,
                    "replies": 12,
                    "meetings": 3,
                    "open_rate": 0.25,
                    "reply_rate": 0.08,
                    "meeting_rate": 0.02
                },
                "variant_b": {
                    "opens": 180,
                    "replies": 18,
                    "meetings": 5,
                    "open_rate": 0.30,
                    "reply_rate": 0.10,
                    "meeting_rate": 0.028
                },
                "winner": "B",
                "confidence_level": 0.95,
                "statistical_significance": True
            }
        },
        {
            "test_id": "ab_test_2",
            "name": "Call-to-Action Test",
            "description": "Testing different CTAs in follow-up emails",
            "base_email_id": "template_2",
            "variants": [
                {
                    "variant_id": "A",
                    "name": "Direct CTA",
                    "cta": "Schedule a 10-minute call",
                    "traffic_percentage": 50
                },
                {
                    "variant_id": "B",
                    "name": "Soft CTA", 
                    "cta": "Would you be interested in a brief chat?",
                    "traffic_percentage": 50
                }
            ],
            "test_duration_days": 5,
            "success_metric": "reply_rate",
            "status": "active",
            "results": None
        }
    ]

@router.post("/niche-researcher/analyze", response_model=NicheResearchResponse)
async def analyze_niche(request: NicheResearchRequest):
    """Analyze and recommend profitable niches"""
    try:
        # Clean and improve the input
        cleaned_input = await clean_and_improve_niche_input(request)
        
        # Call the simple AI API with cleaned input
        ai_response = requests.post(
            "http://localhost:8001/analyze_niche",
            json={
                "skills": cleaned_input["skills"],
                "interests": cleaned_input["interests"],
                "budget": request.budget,
                "experience_level": cleaned_input["experience_level"],
                "time_commitment": request.time_commitment
            },
            timeout=30
        )
        
        if ai_response.status_code == 200:
            data = ai_response.json()
            return NicheResearchResponse(
                recommended_niches=data.get("recommended_niches", []),
                market_analysis=data.get("market_analysis", {}),
                implementation_strategy=data.get("implementation_strategy", []),
                risk_assessment=data.get("risk_assessment", {})
            )
        else:
            raise HTTPException(status_code=500, detail="AI service unavailable")
            
    except requests.exceptions.RequestException:
        # Fallback to mock data if AI service is down, using cleaned input
        return NicheResearchResponse(
            recommended_niches=[
                {
                    "name": f"SaaS for {cleaned_input['interests'][0] if cleaned_input['interests'] else 'Small Businesses'}",
                    "profitability_score": 85,
                    "market_size": "$50B",
                    "competition_level": "Medium",
                    "entry_barrier": "Low",
                    "description": f"B2B software solutions leveraging {', '.join(cleaned_input['skills'][:2]) if cleaned_input['skills'] else 'your skills'}"
                },
                {
                    "name": f"AI-Powered {cleaned_input['interests'][1] if len(cleaned_input['interests']) > 1 else 'Marketing'} Tools",
                    "profitability_score": 90,
                    "market_size": "$25B",
                    "competition_level": "High",
                    "entry_barrier": "Medium",
                    "description": f"Advanced tools combining {', '.join(cleaned_input['skills'][:2]) if cleaned_input['skills'] else 'your expertise'} with AI technology"
                }
            ],
            market_analysis={
                "total_addressable_market": "$75B",
                "growth_rate": "15% annually",
                "key_trends": ["AI integration", "Automation", "Personalization"],
                "target_skills": cleaned_input['skills'],
                "target_interests": cleaned_input['interests']
            },
            implementation_strategy=[
                f"Start with MVP in 3 months focusing on {cleaned_input['interests'][0] if cleaned_input['interests'] else 'your primary interest'}",
                f"Leverage your {cleaned_input['experience_level']} experience in {', '.join(cleaned_input['skills'][:2]) if cleaned_input['skills'] else 'your field'}",
                "Build strong customer feedback loop"
            ],
            risk_assessment={
                "market_risk": "Low",
                "competition_risk": "Medium",
                "technical_risk": "Low"
            }
        )

@router.get("/health")
async def health_check():
    """Health check for AI agents"""
    return {"status": "healthy", "message": "AI Agents service is running"}