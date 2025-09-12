import openai
import json
import os
from typing import Dict, Any, List
import asyncio

class LLMService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_completion(self, system_prompt: str, user_prompt: str, model: str = "gpt-4") -> str:
        """Generate a completion using OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")
    
    async def generate_offer_creator(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate offer using the offer creator template"""
        system_prompt = """You are an expert copywriter specializing in supplement marketing. 
        Create compelling offers that convert while staying compliant with FDA and FTC guidelines.
        
        Return a JSON object with these exact fields:
        - promise: A compelling headline that addresses the pain point
        - proof_pillars: Array of 3-5 proof points (studies, testimonials, guarantees)
        - price: The price with any discounts or bonuses
        - guarantee: A strong guarantee statement
        - cta: A clear call-to-action
        - landing_blurb: A 2-3 sentence description for the landing page
        
        Avoid any health claims, disease claims, or unproven benefits."""
        
        user_prompt = f"""
        Create an offer for:
        - Audience: {inputs.get('audience', '')}
        - Pain Point: {inputs.get('pain', '')}
        - Solution: {inputs.get('solution', '')}
        - Proof: {inputs.get('proof', '')}
        - Price: {inputs.get('price', '')}
        - Guarantee: {inputs.get('guarantee', '')}
        """
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def generate_cold_email(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cold email using the cold email template"""
        system_prompt = """You are an expert cold email writer for supplement marketing.
        Create compelling cold emails that get opened and generate responses.
        
        Return a JSON object with these exact fields:
        - subject: Subject line under 45 characters
        - body: Email body under 90 words
        - tone: The tone used (professional, casual, urgent, etc.)
        - compliance_notes: Any compliance considerations
        
        Avoid spam triggers and ensure compliance with CAN-SPAM and FTC guidelines."""
        
        user_prompt = f"""
        Create a cold email for:
        - Audience: {inputs.get('audience', '')}
        - Pain Point: {inputs.get('pain', '')}
        - Proof: {inputs.get('proof', '')}
        - CTA: {inputs.get('cta', '')}
        """
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def generate_ad_variants(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate three ad variants using the ad writer template"""
        system_prompt = """You are an expert ad copywriter for supplement marketing.
        Create three different ad variants with different angles.
        
        Return a JSON object with these exact fields:
        - proof_based: Object with hook, body, cta, targeting_hints
        - transformation: Object with hook, body, cta, targeting_hints  
        - social_proof: Object with hook, body, cta, targeting_hints
        
        Each variant should have a different psychological angle while staying compliant."""
        
        user_prompt = f"""
        Create three ad variants for:
        - Channel: {inputs.get('channel', '')}
        - Audience: {inputs.get('audience', '')}
        - Pain/Benefit: {inputs.get('pain_or_benefit', '')}
        """
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def generate_workflow(self, description: str) -> Dict[str, Any]:
        """Generate n8n workflow JSON from description"""
        system_prompt = """You are an expert n8n workflow designer.
        Convert plain English descriptions into valid n8n workflow JSON.
        
        Return a JSON object with these exact fields:
        - nodes: Array of n8n node objects with proper structure
        - connections: Object defining connections between nodes
        - summary: Brief description of what the workflow does
        
        Use standard n8n node types like Webhook, HTTP Request, Slack, etc."""
        
        user_prompt = f"Create an n8n workflow for: {description}"
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def score_content(self, content: str) -> Dict[str, float]:
        """Score content on various rubrics"""
        system_prompt = """You are an expert content evaluator for supplement marketing.
        Score the content on a scale of 0-1 for each criterion.
        
        Return a JSON object with these exact fields:
        - clarity: How clear and understandable the content is
        - specificity: How specific and detailed the content is
        - compliance: How compliant with FDA/FTC guidelines
        - brand_match: How well it matches professional brand standards
        
        Be objective and provide scores based on industry standards."""
        
        user_prompt = f"Score this content: {content}"
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def check_compliance(self, content: str) -> Dict[str, Any]:
        """Check content for compliance issues"""
        system_prompt = """You are a compliance expert for supplement marketing.
        Check content for FDA and FTC violations.
        
        Return a JSON object with these exact fields:
        - risk_score: Number from 0-1 (0=low risk, 1=high risk)
        - findings: Array of specific compliance issues found
        - suggested_rewrite: Improved version that removes risks while preserving intent
        
        Look for: disease claims, unproven benefits, dosage claims without citations, 
        before/after language, implied cures, misleading statements."""
        
        user_prompt = f"Check compliance for: {content}"
        
        response = await self.generate_completion(system_prompt, user_prompt)
        return json.loads(response)
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Embedding generation failed: {str(e)}")
