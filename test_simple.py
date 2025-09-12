#!/usr/bin/env python3
"""
Simple test of the LLM service without database dependencies
"""

import os
import sys
sys.path.append('backend')

# Set the API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

from backend.services.llm_service import LLMService
import asyncio
import json

async def test_llm_service():
    """Test the LLM service directly"""
    print("🤖 Testing LLM Service with your OpenAI API key")
    print("=" * 50)
    
    llm_service = LLMService()
    
    # Test offer creator
    print("\n🎯 Testing Offer Creator...")
    try:
        offer_inputs = {
            "audience": "busy professionals aged 30-50 struggling with belly fat",
            "pain": "tried every diet but can't lose stubborn belly fat",
            "solution": "fat loss supplement with clinically-proven ingredients",
            "proof": "clinical study shows 12% more fat loss, 10,000+ customers, 30-day guarantee",
            "price": "$97 with 50% discount for first-time buyers",
            "guarantee": "30-day money-back guarantee"
        }
        
        result = await llm_service.generate_offer_creator(offer_inputs)
        print("✅ Offer Creator Success!")
        print("Generated Offer:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Offer Creator Failed: {e}")
    
    # Test cold email
    print("\n📧 Testing Cold Email Writer...")
    try:
        email_inputs = {
            "audience": "fitness enthusiasts hitting muscle plateaus",
            "pain": "working out hard but not seeing muscle gains",
            "proof": "proven formula used by 5,000+ athletes",
            "cta": "schedule a free consultation"
        }
        
        result = await llm_service.generate_cold_email(email_inputs)
        print("✅ Cold Email Writer Success!")
        print("Generated Email:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Cold Email Writer Failed: {e}")
    
    # Test ad writer
    print("\n📢 Testing Ad Writer...")
    try:
        ad_inputs = {
            "channel": "Meta Facebook",
            "audience": "men 25-45 interested in fitness and supplements",
            "pain_or_benefit": "muscle building and strength gains"
        }
        
        result = await llm_service.generate_ad_variants(ad_inputs)
        print("✅ Ad Writer Success!")
        print("Generated Ad Variants:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Ad Writer Failed: {e}")
    
    # Test compliance check
    print("\n🔒 Testing Compliance Checker...")
    try:
        test_content = "Lose 20 pounds in 30 days with our miracle fat burner!"
        result = await llm_service.check_compliance(test_content)
        print("✅ Compliance Checker Success!")
        print("Compliance Result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Compliance Checker Failed: {e}")
    
    print("\n🎉 LLM Service Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_llm_service())
