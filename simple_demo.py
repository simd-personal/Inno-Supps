#!/usr/bin/env python3
"""
Simple demo server that shows what the API should return
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os

# Set the API key
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')

class DemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
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
                            "audience": {"type": "string"},
                            "pain": {"type": "string"},
                            "solution": {"type": "string"},
                            "proof": {"type": "string"},
                            "price": {"type": "string"},
                            "guarantee": {"type": "string"}
                        }
                    }
                }
            ]
            self.wfile.write(json.dumps(templates).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/generations/generate':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Mock response based on template
            response = {
                "id": "demo-123",
                "template_id": "offer_creator_v1",
                "inputs": {"audience": "test"},
                "output": {
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
                },
                "score": 0.85,
                "compliance_risk": 0.2,
                "status": "completed",
                "created_at": "2024-01-01T00:00:00Z"
            }
            self.wfile.write(json.dumps(response).encode())
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
    server = HTTPServer(('localhost', 8000), DemoHandler)
    print("🚀 Demo API Server running at http://localhost:8000")
    print("📋 Available endpoints:")
    print("   GET  /health")
    print("   GET  /api/templates")
    print("   POST /api/generations/generate")
    print("\n🎯 Now start the frontend in another terminal:")
    print("   cd frontend && npm run dev")
    print("\nThen visit: http://localhost:3000")
    server.serve_forever()
