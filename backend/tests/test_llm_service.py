import pytest
from unittest.mock import AsyncMock, patch
from services.llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.mark.asyncio
async def test_generate_offer_creator(llm_service):
    """Test offer creator generation"""
    inputs = {
        "audience": "busy professionals",
        "pain": "weight loss struggles",
        "solution": "fat loss supplement",
        "proof": "clinical studies",
        "price": "$97",
        "guarantee": "30-day guarantee"
    }
    
    with patch.object(llm_service, 'generate_completion') as mock_generate:
        mock_generate.return_value = '{"promise": "Test Promise", "proof_pillars": ["Study 1"], "price": "$97", "guarantee": "30-day", "cta": "Buy Now", "landing_blurb": "Test blurb"}'
        
        result = await llm_service.generate_offer_creator(inputs)
        
        assert result["promise"] == "Test Promise"
        assert len(result["proof_pillars"]) == 1
        assert result["price"] == "$97"

@pytest.mark.asyncio
async def test_generate_cold_email(llm_service):
    """Test cold email generation"""
    inputs = {
        "audience": "fitness enthusiasts",
        "pain": "muscle plateau",
        "proof": "proven formula",
        "cta": "schedule call"
    }
    
    with patch.object(llm_service, 'generate_completion') as mock_generate:
        mock_generate.return_value = '{"subject": "Test Subject", "body": "Test body", "tone": "professional", "compliance_notes": "Low risk"}'
        
        result = await llm_service.generate_cold_email(inputs)
        
        assert result["subject"] == "Test Subject"
        assert result["body"] == "Test body"
        assert result["tone"] == "professional"

@pytest.mark.asyncio
async def test_score_content(llm_service):
    """Test content scoring"""
    content = "Test content for scoring"
    
    with patch.object(llm_service, 'generate_completion') as mock_generate:
        mock_generate.return_value = '{"clarity": 0.8, "specificity": 0.7, "compliance": 0.9, "brand_match": 0.8}'
        
        result = await llm_service.score_content(content)
        
        assert result["clarity"] == 0.8
        assert result["specificity"] == 0.7
        assert result["compliance"] == 0.9
        assert result["brand_match"] == 0.8

@pytest.mark.asyncio
async def test_check_compliance(llm_service):
    """Test compliance checking"""
    content = "Lose 20 pounds in 30 days!"
    
    with patch.object(llm_service, 'generate_completion') as mock_generate:
        mock_generate.return_value = '{"risk_score": 0.8, "findings": ["Weight loss claim"], "suggested_rewrite": "Supports healthy weight management"}'
        
        result = await llm_service.check_compliance(content)
        
        assert result["risk_score"] == 0.8
        assert len(result["findings"]) == 1
        assert "weight management" in result["suggested_rewrite"].lower()
