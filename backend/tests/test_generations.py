import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app

client = TestClient(app)

@pytest.fixture
def mock_generation_data():
    return {
        "template_id": "offer_creator_v1",
        "inputs": {
            "audience": "test audience",
            "pain": "test pain",
            "solution": "test solution",
            "proof": "test proof",
            "price": "test price",
            "guarantee": "test guarantee"
        }
    }

@pytest.fixture
def mock_llm_response():
    return {
        "promise": "Test Promise",
        "proof_pillars": ["Study 1", "Study 2"],
        "price": "$97",
        "guarantee": "30-day guarantee",
        "cta": "Buy Now",
        "landing_blurb": "Test landing blurb"
    }

def test_generate_offer_creator(mock_generation_data, mock_llm_response):
    """Test offer creator generation endpoint"""
    with patch('services.llm_service.LLMService.generate_offer_creator') as mock_generate:
        mock_generate.return_value = mock_llm_response
        
        response = client.post("/api/generations/generate", json=mock_generation_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["output"]["promise"] == "Test Promise"
        assert len(data["output"]["proof_pillars"]) == 2

def test_score_content():
    """Test content scoring endpoint"""
    score_data = {"content": "Test content for scoring"}
    
    with patch('services.llm_service.LLMService.score_content') as mock_score:
        mock_score.return_value = {
            "clarity": 0.8,
            "specificity": 0.7,
            "compliance": 0.9,
            "brand_match": 0.8
        }
        
        response = client.post("/api/generations/score", json=score_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["clarity"] == 0.8
        assert data["compliance"] == 0.9

def test_compliance_check():
    """Test compliance checking endpoint"""
    compliance_data = {"content": "Lose 20 pounds in 30 days!"}
    
    with patch('services.llm_service.LLMService.check_compliance') as mock_check:
        mock_check.return_value = {
            "risk_score": 0.8,
            "findings": ["Weight loss claim"],
            "suggested_rewrite": "Supports healthy weight management"
        }
        
        response = client.post("/api/compliance/check", json=compliance_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["risk_score"] == 0.8
        assert len(data["findings"]) == 1

def test_workflow_generation():
    """Test workflow generation endpoint"""
    workflow_data = {"description": "Send email when form is submitted"}
    
    with patch('services.llm_service.LLMService.generate_workflow') as mock_workflow:
        mock_workflow.return_value = {
            "nodes": [{"id": "1", "type": "webhook", "name": "Webhook"}],
            "connections": {"1": ["2"]},
            "summary": "Test workflow"
        }
        
        response = client.post("/api/workflows/generate", json=workflow_data)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["nodes"]) == 1
        assert data["summary"] == "Test workflow"
