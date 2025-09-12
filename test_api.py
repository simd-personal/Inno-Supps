#!/usr/bin/env python3
"""
Simple test script to demonstrate what the API should return
"""

import json

def test_offer_creator():
    """Test what the Offer Creator should return"""
    print("🎯 Offer Creator Test")
    print("=" * 40)
    
    # Mock input
    inputs = {
        "audience": "busy professionals aged 30-50 struggling with belly fat",
        "pain": "tried every diet but can't lose stubborn belly fat",
        "solution": "fat loss supplement with clinically-proven ingredients",
        "proof": "clinical study shows 12% more fat loss, 10,000+ customers, 30-day guarantee",
        "price": "$97 with 50% discount for first-time buyers",
        "guarantee": "30-day money-back guarantee"
    }
    
    print("Input:")
    print(json.dumps(inputs, indent=2))
    
    # Expected output
    expected_output = {
        "promise": "Finally Lose Stubborn Belly Fat in 30 Days - Guaranteed",
        "proof_pillars": [
            "Clinical study shows 12% more fat loss",
            "10,000+ customers lost 15+ lbs",
            "30-day money-back guarantee"
        ],
        "price": "$97 (50% off - Limited Time)",
        "guarantee": "30-day money-back guarantee",
        "cta": "Start Your Transformation Today",
        "landing_blurb": "Join thousands who've finally lost stubborn belly fat with our clinically-proven formula. 30-day guarantee."
    }
    
    print("\nExpected Output:")
    print(json.dumps(expected_output, indent=2))
    print()

def test_cold_email():
    """Test what the Cold Email Writer should return"""
    print("📧 Cold Email Writer Test")
    print("=" * 40)
    
    inputs = {
        "audience": "fitness enthusiasts hitting muscle plateaus",
        "pain": "working out hard but not seeing muscle gains",
        "proof": "proven formula used by 5,000+ athletes",
        "cta": "schedule a free consultation"
    }
    
    print("Input:")
    print(json.dumps(inputs, indent=2))
    
    expected_output = {
        "subject": "Break Through Your Muscle Plateau",
        "body": "Hi [Name], I noticed you're serious about fitness but hitting a plateau. Our clients typically see 20% more gains in 8 weeks. Want to learn how?",
        "tone": "professional but friendly",
        "compliance_notes": "Avoid specific claims about muscle growth percentages"
    }
    
    print("\nExpected Output:")
    print(json.dumps(expected_output, indent=2))
    print()

def test_ad_writer():
    """Test what the Ad Writer should return"""
    print("📢 Ad Writer Test")
    print("=" * 40)
    
    inputs = {
        "channel": "Meta Facebook",
        "audience": "men 25-45 interested in fitness and supplements",
        "pain_or_benefit": "muscle building and strength gains"
    }
    
    print("Input:")
    print(json.dumps(inputs, indent=2))
    
    expected_output = {
        "proof_based": {
            "hook": "Science-Backed Muscle Growth Formula",
            "body": "Clinical study shows 23% more muscle mass in 8 weeks",
            "cta": "Get Your Free Sample",
            "targeting_hints": "Fitness enthusiasts, gym-goers, bodybuilders"
        },
        "transformation": {
            "hook": "From Skinny to Strong in 60 Days",
            "body": "See the transformation that changed everything",
            "cta": "Start Your Journey",
            "targeting_hints": "Men 25-45, fitness beginners, transformation seekers"
        },
        "social_proof": {
            "hook": "Join 10,000+ Men Who Built Muscle",
            "body": "Real results from real people - see their stories",
            "cta": "Join the Community",
            "targeting_hints": "Social proof seekers, community builders, success stories"
        }
    }
    
    print("\nExpected Output:")
    print(json.dumps(expected_output, indent=2))
    print()

def test_workflow_builder():
    """Test what the Workflow Builder should return"""
    print("🔄 Workflow Builder Test")
    print("=" * 40)
    
    inputs = {
        "description": "When a new lead fills out the fat loss supplement form, send them a welcome email, add them to the CRM, and notify the sales team in Slack"
    }
    
    print("Input:")
    print(json.dumps(inputs, indent=2))
    
    expected_output = {
        "nodes": [
            {
                "id": "webhook-trigger",
                "type": "n8n-nodes-base.webhook",
                "name": "Form Submission",
                "parameters": {
                    "path": "fat-loss-form",
                    "httpMethod": "POST"
                }
            },
            {
                "id": "welcome-email",
                "type": "n8n-nodes-base.emailSend",
                "name": "Send Welcome Email",
                "parameters": {
                    "subject": "Welcome to Your Fat Loss Journey!",
                    "message": "Thank you for your interest in our fat loss supplement..."
                }
            },
            {
                "id": "crm-add",
                "type": "n8n-nodes-base.hubspot",
                "name": "Add to CRM",
                "parameters": {
                    "operation": "create",
                    "resource": "contact"
                }
            },
            {
                "id": "slack-notify",
                "type": "n8n-nodes-base.slack",
                "name": "Notify Sales Team",
                "parameters": {
                    "channel": "#sales-alerts",
                    "text": "New fat loss lead: {{ $json.email }}"
                }
            }
        ],
        "connections": {
            "webhook-trigger": ["welcome-email", "crm-add"],
            "crm-add": ["slack-notify"]
        },
        "summary": "Lead processing workflow that sends welcome email, adds contact to CRM, and notifies sales team via Slack"
    }
    
    print("\nExpected Output:")
    print(json.dumps(expected_output, indent=2))
    print()

def test_slack_summary():
    """Test what the Slack summary should return"""
    print("💬 Slack Summary Test")
    print("=" * 40)
    
    expected_output = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📊 Daily Inno Supps Summary"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*🏆 Top Performing Campaigns (by Adjusted ROAS)*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "1. *Fat Loss Pro* - ROAS: 4.2x, Margin: 60%, Adj ROAS: 2.52x"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "2. *Muscle Builder* - ROAS: 3.8x, Margin: 55%, Adj ROAS: 2.09x"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "3. *Energy Boost* - ROAS: 5.1x, Margin: 70%, Adj ROAS: 3.57x"
                }
            }
        ]
    }
    
    print("Expected Slack Summary:")
    print(json.dumps(expected_output, indent=2))
    print()

if __name__ == "__main__":
    print("🚀 Inno Supps PromptOps MVP - What Should Be Working")
    print("=" * 60)
    print()
    
    test_offer_creator()
    test_cold_email()
    test_ad_writer()
    test_workflow_builder()
    test_slack_summary()
    
    print("✅ All modules should work as shown above!")
    print()
    print("🔧 To get started:")
    print("1. Set up OpenAI API key in .env file")
    print("2. Run: docker-compose up -d")
    print("3. Visit: http://localhost:3000")
    print("4. Test each module with the inputs shown above")
