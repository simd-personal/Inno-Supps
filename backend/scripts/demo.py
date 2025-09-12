#!/usr/bin/env python3
"""
Demo script for Inno Supps PromptOps MVP
Demonstrates the complete workflow from offer creation to n8n workflow import
"""

import sys
import os
import asyncio
import httpx
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"

async def demo_workflow():
    """Run the complete demo workflow"""
    print("🚀 Starting Inno Supps PromptOps MVP Demo")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # 1. Create an offer for a fat loss product
        print("\n1. Creating offer for fat loss product...")
        offer_response = await client.post(f"{BASE_URL}/api/generations/generate", json={
            "template_id": "offer_creator_v1",  # This would be the actual template ID
            "inputs": {
                "audience": "busy professionals aged 30-50 struggling with belly fat",
                "pain": "tried every diet but can't lose stubborn belly fat",
                "solution": "fat loss supplement with clinically-proven ingredients",
                "proof": "clinical study shows 12% more fat loss, 10,000+ customers, 30-day guarantee",
                "price": "$97 with 50% discount for first-time buyers",
                "guarantee": "30-day money-back guarantee"
            }
        })
        
        if offer_response.status_code == 200:
            offer_data = offer_response.json()
            print("✅ Offer created successfully!")
            print(f"   Promise: {offer_data['output']['promise']}")
            print(f"   Price: {offer_data['output']['price']}")
        else:
            print(f"❌ Offer creation failed: {offer_response.text}")
            return
        
        # 2. Generate cold email
        print("\n2. Generating cold email...")
        email_response = await client.post(f"{BASE_URL}/api/generations/generate", json={
            "template_id": "cold_email_v1",
            "inputs": {
                "audience": "fitness enthusiasts hitting muscle plateaus",
                "pain": "working out hard but not seeing muscle gains",
                "proof": "proven formula used by 5,000+ athletes",
                "cta": "schedule a free consultation"
            }
        })
        
        if email_response.status_code == 200:
            email_data = email_response.json()
            print("✅ Cold email generated successfully!")
            print(f"   Subject: {email_data['output']['subject']}")
            print(f"   Body: {email_data['output']['body']}")
        else:
            print(f"❌ Email generation failed: {email_response.text}")
            return
        
        # 3. Generate ad variants
        print("\n3. Generating ad variants...")
        ads_response = await client.post(f"{BASE_URL}/api/generations/generate", json={
            "template_id": "ad_writer_v1",
            "inputs": {
                "channel": "Meta Facebook",
                "audience": "men 25-45 interested in fitness and supplements",
                "pain_or_benefit": "muscle building and strength gains"
            }
        })
        
        if ads_response.status_code == 200:
            ads_data = ads_response.json()
            print("✅ Ad variants generated successfully!")
            print("   Variants:")
            for variant_name, variant_data in ads_data['output'].items():
                print(f"   - {variant_name}: {variant_data['hook']}")
        else:
            print(f"❌ Ad generation failed: {ads_response.text}")
            return
        
        # 4. Generate n8n workflow
        print("\n4. Generating n8n workflow...")
        workflow_response = await client.post(f"{BASE_URL}/api/workflows/generate", json={
            "description": "When a new lead fills out the fat loss supplement form, send them a welcome email, add them to the CRM, and notify the sales team in Slack"
        })
        
        if workflow_response.status_code == 200:
            workflow_data = workflow_response.json()
            print("✅ Workflow generated successfully!")
            print(f"   Summary: {workflow_data['summary']}")
            print(f"   Nodes: {len(workflow_data['nodes'])}")
        else:
            print(f"❌ Workflow generation failed: {workflow_response.text}")
            return
        
        # 5. Import workflow to n8n
        print("\n5. Importing workflow to n8n...")
        import_response = await client.post(f"{BASE_URL}/api/workflows/import", json={
            "workflow_json": {
                "name": "Fat Loss Lead Processing",
                "nodes": workflow_data['nodes'],
                "connections": workflow_data['connections']
            }
        })
        
        if import_response.status_code == 200:
            import_data = import_response.json()
            print("✅ Workflow imported to n8n successfully!")
            print(f"   Workflow ID: {import_data['workflow_id']}")
        else:
            print(f"❌ Workflow import failed: {import_response.text}")
            return
        
        # 6. Check compliance
        print("\n6. Checking compliance...")
        compliance_response = await client.post(f"{BASE_URL}/api/compliance/check", json={
            "content": "Lose 20 pounds in 30 days with our miracle fat burner!"
        })
        
        if compliance_response.status_code == 200:
            compliance_data = compliance_response.json()
            print("✅ Compliance check completed!")
            print(f"   Risk Score: {compliance_data['risk_score']:.2f}")
            print(f"   Issues: {len(compliance_data['findings'])}")
        else:
            print(f"❌ Compliance check failed: {compliance_response.text}")
            return
        
        # 7. Get daily summary
        print("\n7. Getting daily summary...")
        summary_response = await client.post(f"{BASE_URL}/api/slack/command", data={
            "command": "/inno",
            "text": "summary today"
        })
        
        if summary_response.status_code == 200:
            summary_data = summary_response.json()
            print("✅ Daily summary generated!")
            print("   Check Slack for the full summary")
        else:
            print(f"❌ Summary generation failed: {summary_response.text}")
            return
        
        print("\n🎉 Demo completed successfully!")
        print("=" * 50)
        print("All systems are working correctly:")
        print("✅ Offer Creator")
        print("✅ Cold Email Writer") 
        print("✅ Ad Writer")
        print("✅ Workflow Builder")
        print("✅ n8n Integration")
        print("✅ Compliance Checker")
        print("✅ Slack Integration")

if __name__ == "__main__":
    asyncio.run(demo_workflow())
