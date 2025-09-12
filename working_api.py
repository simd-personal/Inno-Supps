#!/usr/bin/env python3
"""
Working API server without database dependencies
"""

import os
import json
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
sys.path.append('backend')

# Set the API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

from backend.services.llm_service import LLMService

class WorkingAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.llm_service = LLMService()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "message": "Inno Supps API is running"}).encode())
        
        elif self.path == '/api/templates':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            templates = [
                {
                    "id": "offer_creator_v1",
                    "name": "offer_creator_v1",
                    "version": "1.0",
                    "schema_json": {
                        "type": "object",
                        "properties": {
                            "audience": {"type": "string", "description": "Target audience"},
                            "pain": {"type": "string", "description": "Pain point to address"},
                            "solution": {"type": "string", "description": "Product/solution"},
                            "proof": {"type": "string", "description": "Proof points"},
                            "price": {"type": "string", "description": "Price point"},
                            "guarantee": {"type": "string", "description": "Guarantee offer"}
                        },
                        "required": ["audience", "pain", "solution", "proof", "price", "guarantee"]
                    },
                    "system_prompt": "You are an expert copywriter specializing in supplement marketing...",
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "promise": {"type": "string"},
                            "proof_pillars": {"type": "array", "items": {"type": "string"}},
                            "price": {"type": "string"},
                            "guarantee": {"type": "string"},
                            "cta": {"type": "string"},
                            "landing_blurb": {"type": "string"}
                        }
                    }
                },
                {
                    "id": "cold_email_v1",
                    "name": "cold_email_v1",
                    "version": "1.0",
                    "schema_json": {
                        "type": "object",
                        "properties": {
                            "audience": {"type": "string", "description": "Target audience"},
                            "pain": {"type": "string", "description": "Pain point"},
                            "proof": {"type": "string", "description": "Proof points"},
                            "cta": {"type": "string", "description": "Call to action"}
                        },
                        "required": ["audience", "pain", "proof", "cta"]
                    },
                    "system_prompt": "You are an expert cold email writer for supplement marketing...",
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "body": {"type": "string"},
                            "tone": {"type": "string"},
                            "compliance_notes": {"type": "string"}
                        }
                    }
                },
                {
                    "id": "ad_writer_v1",
                    "name": "ad_writer_v1",
                    "version": "1.0",
                    "schema_json": {
                        "type": "object",
                        "properties": {
                            "channel": {"type": "string", "description": "Advertising channel"},
                            "audience": {"type": "string", "description": "Target audience"},
                            "pain_or_benefit": {"type": "string", "description": "Pain point or benefit"}
                        },
                        "required": ["channel", "audience", "pain_or_benefit"]
                    },
                    "system_prompt": "You are an expert ad copywriter for supplement marketing...",
                    "output_schema": {
                        "type": "object",
                        "properties": {
                            "proof_based": {"type": "object"},
                            "transformation": {"type": "object"},
                            "social_proof": {"type": "object"}
                        }
                    }
                }
            ]
            self.wfile.write(json.dumps(templates).encode())
        
        elif self.path == '/api/generations':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Return empty list for now
            self.wfile.write(json.dumps([]).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/generations/generate':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Generate content based on template
                template_id = data.get('template_id')
                inputs = data.get('inputs', {})
                
                if template_id == 'offer_creator_v1':
                    result = asyncio.run(self.llm_service.generate_offer_creator(inputs))
                elif template_id == 'cold_email_v1':
                    result = asyncio.run(self.llm_service.generate_cold_email(inputs))
                elif template_id == 'ad_writer_v1':
                    result = asyncio.run(self.llm_service.generate_ad_variants(inputs))
                else:
                    result = {"error": "Unknown template"}
                
                response = {
                    "id": "demo-123",
                    "template_id": template_id,
                    "inputs": inputs,
                    "output": result,
                    "score": 0.85,
                    "compliance_risk": 0.2,
                    "status": "completed",
                    "created_at": "2024-01-01T00:00:00Z"
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
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path == '/api/generations/score':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                content = data.get('content', '')
                result = asyncio.run(self.llm_service.score_content(content))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        
        elif self.path == '/api/compliance/check':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                content = data.get('content', '')
                result = asyncio.run(self.llm_service.check_compliance(content))
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {"error": str(e)}
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
    server = HTTPServer(('localhost', 8000), WorkingAPIHandler)
    print("🚀 Working API Server running at http://localhost:8000")
    print("📋 Available endpoints:")
    print("   GET  /health")
    print("   GET  /api/templates")
    print("   GET  /api/generations")
    print("   POST /api/generations/generate")
    print("   POST /api/generations/score")
    print("   POST /api/compliance/check")
    print("\n🎯 Now start the frontend:")
    print("   cd frontend && npm run dev")
    print("\nThen visit: http://localhost:3000")
    server.serve_forever()
