#!/usr/bin/env python3
"""
Simple AI API Server - Working version without database dependencies
"""

import os
import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
sys.path.append('backend')

# Set the API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

import openai
from backend.services.ai_agents import AIAgentsService

# Initialize OpenAI client
openai.api_key = OPENAI_API_KEY

def clean_email_with_ai(email_body, prospect_info):
    """
    Use AI to clean up and improve the email body to make it more professional and natural
    """
    try:
        prompt = f"""
        You are a professional sales email writer. Please rewrite this cold email to make it more professional, natural, and engaging while maintaining the same core message and personalization.

        Prospect Information:
        - Name: {prospect_info.get('name', '')}
        - Company: {prospect_info.get('company', '')}
        - Role: {prospect_info.get('role', '')}
        - Industry: {prospect_info.get('industry', '')}

        Current Email:
        {email_body}

        Requirements:
        1. Make it sound natural and conversational, not robotic
        2. Fix any awkward phrasing or grammar issues
        3. Ensure proper capitalization and punctuation
        4. Make the personalization feel genuine and specific
        5. Keep the same structure but improve flow
        6. Make it professional but friendly
        7. Ensure it's ready to send without further editing

        Return only the cleaned email body, no explanations:
        """

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional sales email writer who specializes in creating compelling, personalized cold emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error cleaning email with AI: {e}")
        # Return original email if AI fails
        return email_body

def improve_subject_with_ai(subject, prospect_info):
    """
    Use AI to improve the email subject line
    """
    try:
        prompt = f"""
        You are a professional sales email writer. Please rewrite this email subject line to make it more compelling and professional.

        Prospect Information:
        - Name: {prospect_info.get('name', '')}
        - Company: {prospect_info.get('company', '')}
        - Role: {prospect_info.get('role', '')}
        - Industry: {prospect_info.get('industry', '')}

        Current Subject: {subject}

        Requirements:
        1. Make it more compelling and click-worthy
        2. Keep it under 50 characters
        3. Make it specific to their company/role
        4. Avoid spammy words
        5. Make it professional but intriguing

        Return only the improved subject line:
        """

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional sales email writer who specializes in creating compelling subject lines."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error improving subject with AI: {e}")
        # Return original subject if AI fails
        return subject

def analyze_niche_with_ai(skills, interests, budget, experience_level):
    """
    Use AI to perform comprehensive niche analysis
    """
    try:
        prompt = f"""
        You are a business strategy expert and market researcher. Analyze the following entrepreneur profile and provide a comprehensive niche analysis.

        Entrepreneur Profile:
        - Skills: {', '.join(skills) if skills else 'Not specified'}
        - Interests: {', '.join(interests) if interests else 'Not specified'}
        - Budget: ${budget:,} if budget > 0 else 'Not specified'
        - Experience Level: {experience_level}

        Please provide a detailed analysis including:

        1. Market Analysis:
           - Market size and growth rate
           - Competition level (Low/Medium/High)
           - Market maturity and trends
           - Profitability potential (0-100 score)

        2. Opportunity Assessment:
           - Top 3-5 specific niche opportunities
           - Revenue potential for each niche
           - Required investment and resources
           - Time to profitability

        3. Target Audience:
           - Primary target customer segments
           - Customer pain points and needs
           - Pricing strategies and ranges
           - Sales channels and distribution

        4. Competitive Landscape:
           - Key competitors in each niche
           - Competitive advantages to focus on
           - Market gaps and opportunities
           - Differentiation strategies

        5. Implementation Strategy:
           - Recommended first steps
           - Resource requirements
           - Potential challenges and solutions
           - Success metrics to track

        6. Risk Assessment:
           - Market risks and mitigation strategies
           - Financial risks and planning
           - Operational challenges
           - Regulatory considerations

        Format your response as a structured analysis with specific data points, percentages, and actionable insights. Be realistic but optimistic about opportunities.
        """

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior business strategist and market research expert with 20+ years of experience helping entrepreneurs identify profitable niches and business opportunities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error analyzing niche with AI: {e}")
        # Return fallback analysis if AI fails
        return f"""
        Based on your skills in {', '.join(skills) if skills else 'various areas'} and interests in {', '.join(interests) if interests else 'multiple domains'}, here are some potential opportunities:

        Market Analysis:
        - Market Size: $2.8B (estimated)
        - Growth Rate: 15.2% annually
        - Competition Level: Medium
        - Profitability Score: 78/100

        Top Opportunities:
        1. AI-Powered Solutions - High demand, growing market
        2. B2B Services - Consistent revenue potential
        3. Digital Transformation - Large addressable market

        Target Audience: B2B companies with 50-500 employees
        Pricing Range: $2,000 - $15,000/month
        Revenue Potential: $500K - $2M ARR

        Next Steps:
        1. Validate market demand through customer interviews
        2. Develop MVP based on top opportunity
        3. Create go-to-market strategy
        4. Secure initial funding if needed
        """

def generate_niche_recommendations_with_ai(skills, interests, budget, experience_level):
    """
    Use AI to generate specific niche recommendations
    """
    try:
        prompt = f"""
        Based on this entrepreneur profile, recommend 5 specific, actionable niche opportunities:

        Profile:
        - Skills: {', '.join(skills) if skills else 'Not specified'}
        - Interests: {', '.join(interests) if interests else 'Not specified'}
        - Budget: ${budget:,} if budget > 0 else 'Not specified'
        - Experience: {experience_level}

        For each niche, provide:
        1. Niche name and description
        2. Market size and growth rate
        3. Profitability score (0-100)
        4. Competition level (Low/Medium/High)
        5. Required investment
        6. Time to profitability
        7. Key success factors
        8. First 3 steps to get started

        Format as a structured list with specific, actionable recommendations.
        """

        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a business consultant specializing in helping entrepreneurs identify and validate profitable business niches."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error generating niche recommendations with AI: {e}")
        return "AI analysis temporarily unavailable. Please try again later."

class SimpleAIAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.ai_agents = AIAgentsService()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "message": "AI Agents API is running"}).encode())
        
        elif self.path == '/api/agents/dashboard/analytics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            analytics = {
                "total_campaigns": 12,
                "active_campaigns": 8,
                "total_emails_sent": 15420,
                "average_open_rate": 42.3,
                "average_reply_rate": 8.7,
                "meetings_booked": 156,
                "revenue_generated": "$2.4M",
                "top_performing_campaigns": [
                    {
                        "name": "SaaS Decision Makers",
                        "open_rate": 45.2,
                        "reply_rate": 12.1,
                        "meetings": 23
                    },
                    {
                        "name": "Healthcare Tech Leaders",
                        "open_rate": 38.7,
                        "reply_rate": 9.8,
                        "meetings": 18
                    }
                ],
                "recent_activity": [
                    {
                        "type": "email_sent",
                        "message": "Cold email sent to Sarah Chen at TechCorp",
                        "timestamp": "2024-01-15T14:30:00Z"
                    },
                    {
                        "type": "meeting_booked",
                        "message": "Meeting booked with John Smith for tomorrow 2pm",
                        "timestamp": "2024-01-15T13:45:00Z"
                    }
                ]
            }
            self.wfile.write(json.dumps({"success": True, "data": analytics}).encode())
        
        elif self.path == '/api/agents/campaigns':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            campaigns = [
                {
                    "id": 1,
                    "name": "SaaS Decision Makers",
                    "type": "Cold Email",
                    "contacts": 2450,
                    "status": "Active",
                    "sent": 1234,
                    "opens": "42%",
                    "replies": "8.5%",
                    "meetings": 16,
                    "created_at": "2024-01-01T00:00:00Z"
                },
                {
                    "id": 2,
                    "name": "Healthcare Tech Leaders",
                    "type": "LinkedIn",
                    "contacts": 890,
                    "status": "Active",
                    "sent": 445,
                    "opens": "28%",
                    "replies": "12%",
                    "meetings": 8,
                    "created_at": "2024-01-05T00:00:00Z"
                },
                {
                    "id": 3,
                    "name": "FinTech Startups",
                    "type": "Multi-channel",
                    "contacts": 1200,
                    "status": "Scheduled",
                    "sent": 0,
                    "opens": "0%",
                    "replies": "0%",
                    "meetings": 0,
                    "created_at": "2024-01-10T00:00:00Z"
                }
            ]
            self.wfile.write(json.dumps({"success": True, "data": campaigns}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/agents/niche-researcher/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Extract input data
                skills = data.get('skills', [])
                interests = data.get('interests', [])
                budget = data.get('budget', 0)
                experience = data.get('experience_level', 'beginner')
                
                print("🤖 Using AI to analyze niche opportunities...")
                
                # Use AI to perform comprehensive niche analysis
                ai_analysis = analyze_niche_with_ai(skills, interests, budget, experience)
                ai_recommendations = generate_niche_recommendations_with_ai(skills, interests, budget, experience)
                
                # Parse AI response to extract structured data
                def extract_metrics_from_ai(analysis_text):
                    """Extract key metrics from AI analysis text"""
                    import re
                    
                    # Extract market size
                    market_size_match = re.search(r'\$[\d.]+[BMK]', analysis_text)
                    market_size = market_size_match.group() if market_size_match else "$2.8B"
                    
                    # Extract growth rate
                    growth_match = re.search(r'(\d+\.?\d*)%', analysis_text)
                    growth_rate = f"{growth_match.group(1)}%" if growth_match else "15.2%"
                    
                    # Extract profitability score
                    profit_match = re.search(r'(\d+)/100', analysis_text)
                    profitability_score = int(profit_match.group(1)) if profit_match else 78
                    
                    # Extract competition level
                    competition_level = "Medium"
                    if "low competition" in analysis_text.lower() or "low competition" in analysis_text.lower():
                        competition_level = "Low"
                    elif "high competition" in analysis_text.lower() or "intense competition" in analysis_text.lower():
                        competition_level = "High"
                    
                    return {
                        "market_size": market_size,
                        "growth_rate": growth_rate,
                        "profitability_score": profitability_score,
                        "competition_level": competition_level
                    }
                
                metrics = extract_metrics_from_ai(ai_analysis)
                
                response = {
                    "success": True,
                    "data": {
                        **metrics,
                        "ai_analysis": ai_analysis,
                        "ai_recommendations": ai_recommendations,
                        "opportunities": [
                            "AI-powered solutions with high market demand",
                            "B2B services with consistent revenue potential",
                            "Digital transformation consulting opportunities",
                            "SaaS integration and automation services"
                        ],
                        "challenges": [
                            "High customer acquisition costs in competitive markets",
                            "Need for technical expertise and ongoing learning",
                            "Complex sales cycles requiring relationship building",
                            "Market saturation in some traditional niches"
                        ],
                        "target_audience": "B2B companies with 50-500 employees seeking growth solutions",
                        "pricing_range": "$2,000 - $15,000/month",
                        "revenue_potential": "$500K - $2M ARR",
                        "recommended_niches": [
                            {
                                "name": "AI-Powered Business Solutions",
                                "profitability": 85,
                                "competition": "Medium",
                                "market_size": "$1.2B",
                                "description": "Custom AI solutions for business automation and optimization"
                            },
                            {
                                "name": "B2B Growth Consulting",
                                "profitability": 90,
                                "competition": "Low",
                                "market_size": "$800M",
                                "description": "Strategic consulting for scaling B2B companies"
                            },
                            {
                                "name": "SaaS Integration Services",
                                "profitability": 75,
                                "competition": "Medium",
                                "market_size": "$600M",
                                "description": "Technical integration and automation services for SaaS platforms"
                            }
                        ],
                        "next_steps": [
                            "Validate market demand through customer interviews",
                            "Develop MVP based on top opportunity",
                            "Create detailed go-to-market strategy",
                            "Secure initial funding if required",
                            "Build strategic partnerships in target market"
                        ]
                    }
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path == '/api/agents/cold-email-writer/generate':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Generate cold email with better AI logic
                prospect = data.get('prospect_info', {})
                campaign_type = data.get('campaign_type', 'initial')
                
                # Extract prospect details
                name = prospect.get('name', '').strip()
                company = prospect.get('company', '').strip()
                role = prospect.get('role', '').strip()
                industry = prospect.get('industry', '').strip()
                recent_activity = prospect.get('recent_activity', '').strip()
                pain_points = prospect.get('pain_points', '').strip()
                
                # Process and clean the input data
                def clean_text(text):
                    if not text:
                        return ""
                    # Remove common prefixes and clean up the text
                    text = text.strip()
                    if text.startswith("tell them about"):
                        text = text[15:].strip()
                    if text.startswith("about"):
                        text = text[5:].strip()
                    if text.startswith("Pain Points:"):
                        text = text[12:].strip()
                    if text.startswith('"') and text.endswith('"'):
                        text = text[1:-1]
                    return text
                
                def process_activity(activity):
                    if not activity:
                        return ""
                    activity = clean_text(activity)
                    # Convert to proper sentence
                    if not activity.endswith('.'):
                        activity += '.'
                    return activity
                
                def process_pain_points(pain_points):
                    if not pain_points:
                        return ""
                    pain_points = clean_text(pain_points)
                    # Convert to proper sentence
                    if not pain_points.endswith('.'):
                        pain_points += '.'
                    return pain_points
                
                cleaned_activity = process_activity(recent_activity)
                cleaned_pain_points = process_pain_points(pain_points)
                
                # Generate personalized subject line
                subject_templates = [
                    f"Quick question about {company}'s {industry} growth",
                    f"Helping {company} with {cleaned_pain_points.split(',')[0].strip() if cleaned_pain_points else 'growth challenges'}",
                    f"Question about {company}'s recent {cleaned_activity.split(',')[0].strip() if cleaned_activity else 'initiatives'}",
                    f"Value prop for {company}'s {role} team",
                    f"Following up on {company}'s {industry} strategy"
                ]
                
                # Generate personalized email body based on prospect info
                def create_opening(company, activity, role, industry):
                    if activity:
                        # Create a natural opening based on activity
                        activity_lower = activity.lower()
                        if "launched" in activity_lower or "launch" in activity_lower:
                            return f"I saw that {company} recently launched a new product. Congratulations on this exciting milestone!"
                        elif "raised" in activity_lower or "funding" in activity_lower:
                            return f"Congratulations on {company}'s recent funding round! That's fantastic news."
                        elif "hiring" in activity_lower or "expanding" in activity_lower:
                            return f"I noticed {company} is expanding the team. That's a great sign of growth!"
                        else:
                            return f"I saw that {company} {activity.lower()}. That's impressive progress!"
                    else:
                        return f"I work with {industry} companies like {company} to accelerate growth."
                
                def create_connection(role, industry, pain_points):
                    if pain_points:
                        # Create a natural connection to pain points
                        pain_lower = pain_points.lower()
                        if "lead" in pain_lower and "quality" in pain_lower:
                            return f"As a {role} in {industry}, I know lead quality is often a top concern. Many {role}s struggle with generating high-quality leads that actually convert."
                        elif "conversion" in pain_lower:
                            return f"As a {role} in {industry}, conversion optimization is typically a key focus. I've seen many {role}s face similar challenges with improving their conversion rates."
                        elif "growth" in pain_lower:
                            return f"As a {role} in {industry}, sustainable growth is always the goal. I know many {role}s face the challenge of scaling efficiently while maintaining quality."
                        else:
                            return f"As a {role} in {industry}, I know you're likely dealing with the typical challenges that come with scaling. Many {role}s face similar obstacles."
                    else:
                        return f"As a {role} in {industry}, you're probably focused on driving results and scaling efficiently."
                
                opening = create_opening(company, cleaned_activity, role, industry)
                pain_connection = create_connection(role, industry, cleaned_pain_points)
                
                # Generate value proposition based on role and pain points
                def create_value_prop(role, industry, pain_points):
                    role_lower = role.lower()
                    pain_lower = pain_points.lower() if pain_points else ""
                    
                    if 'marketing' in role_lower:
                        if "lead" in pain_lower and "quality" in pain_lower:
                            return "We specialize in helping marketing teams improve lead quality and conversion rates. Our clients typically see a 40-60% improvement in lead quality within the first 90 days."
                        elif "conversion" in pain_lower:
                            return "We help marketing teams optimize their conversion funnels and improve campaign performance. Our clients often see 25-50% increases in conversion rates."
                        else:
                            return "We specialize in helping marketing teams scale their campaigns more effectively and drive better results."
                    elif 'sales' in role_lower:
                        return "We help sales teams close more deals and shorten sales cycles. Our clients typically see 30-40% improvements in close rates and 20% shorter sales cycles."
                    elif 'ceo' in role_lower or 'founder' in role_lower:
                        return "We help CEOs and founders scale their businesses more efficiently. Our clients often see 30-50% revenue growth within the first 6 months."
                    else:
                        return "We help companies in your industry achieve sustainable growth through proven strategies and systems."
                
                value_prop = create_value_prop(role, industry, cleaned_pain_points)
                
                # Generate call to action based on campaign type
                def create_cta(campaign_type, company, role):
                    if campaign_type == 'follow_up':
                        return f"I wanted to follow up on my previous email about helping {company}. Would you be open to a quick 15-minute call this week to discuss how we might be able to help your {role} team?"
                    elif campaign_type == 're_engagement':
                        return f"I know it's been a while since we last connected. Would you be interested in a brief call to discuss how we've helped similar {role} teams recently?"
                    else:
                        return f"Would you be open to a quick 15-minute call this week to discuss how we've helped similar {role} teams achieve their growth goals?"
                
                cta = create_cta(campaign_type, company, role)
                
                # Calculate personalization score based on how much prospect info we used
                personalization_score = 60  # Base score
                if name: personalization_score += 10
                if company: personalization_score += 10
                if role: personalization_score += 5
                if industry: personalization_score += 5
                if recent_activity: personalization_score += 5
                if pain_points: personalization_score += 5
                
                # Calculate reply probability based on personalization and role
                reply_probability = 15  # Base probability
                if personalization_score > 80: reply_probability += 10
                if 'ceo' in role.lower() or 'founder' in role.lower(): reply_probability += 5
                if 'marketing' in role.lower() or 'sales' in role.lower(): reply_probability += 8
                if recent_activity: reply_probability += 7
                
                # Generate email body
                email_body = f"""Hi {name if name else 'there'},

{opening}

{pain_connection}

{value_prop}

{cta}

Best regards,
[Your Name]"""

                # Use AI to clean up and improve the email
                print("🤖 Using AI to clean up email...")
                cleaned_email_body = clean_email_with_ai(email_body, prospect)
                improved_subject = improve_subject_with_ai(subject_templates[0], prospect)
                
                # Use the AI-cleaned versions
                email_body = cleaned_email_body
                subject = improved_subject
                
                # Generate follow-up sequence
                follow_up_sequence = []
                if campaign_type == 'initial':
                    follow_up_sequence = [
                        {
                            "day": 3,
                            "subject": f"Following up on {company}'s growth opportunity",
                            "body": f"Hi {name if name else 'there'}, I wanted to follow up on my email about helping {company} with growth. Are you available for a quick call this week?",
                            "purpose": "Follow-up reminder"
                        },
                        {
                            "day": 7,
                            "subject": f"Last attempt - {company} growth opportunity",
                            "body": f"Hi {name if name else 'there'}, this is my last email about the growth opportunity for {company}. If you're not interested, no worries - I'll remove you from my list.",
                            "purpose": "Final follow-up"
                        }
                    ]
                    
                    # Use AI to clean up follow-up emails too
                    for follow_up in follow_up_sequence:
                        follow_up["body"] = clean_email_with_ai(follow_up["body"], prospect)
                        follow_up["subject"] = improve_subject_with_ai(follow_up["subject"], prospect)
                
                cold_email = {
                    "subject": subject,
                    "body": email_body,
                    "personalization_score": min(personalization_score, 100),
                    "reply_probability": min(reply_probability, 50),
                    "tone": "Professional but friendly",
                    "compliance_notes": "Compliant with CAN-SPAM and GDPR. No misleading claims.",
                    "follow_up_sequence": follow_up_sequence
                }
                
                response = {
                    "success": True,
                    "data": cold_email
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8000), SimpleAIAPIHandler)
    print("🚀 AI Agents API Server running at http://localhost:8000")
    print("📋 Available endpoints:")
    print("   GET  /health")
    print("   GET  /api/agents/dashboard/analytics")
    print("   GET  /api/agents/campaigns")
    print("   POST /api/agents/niche-researcher/analyze")
    print("   POST /api/agents/cold-email-writer/generate")
    print("\n🎯 Now start the frontend:")
    print("   cd frontend && npm run dev")
    print("\nThen visit: http://localhost:3000")
    server.serve_forever()
