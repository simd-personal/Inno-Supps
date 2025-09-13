"""
Data enrichment providers (Apollo, etc.)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseProvider
from backend.config import settings

class ApolloProvider(BaseProvider):
    """Apollo.io integration provider for data enrichment"""
    
    def test_connection(self) -> bool:
        if self.mock_mode:
            return True
        
        # In production, test Apollo API connection
        try:
            # This would use Apollo API to test connection
            return True
        except Exception:
            return False
    
    def get_status(self) -> str:
        if self.mock_mode:
            return "connected (mock)"
        return "connected" if self.test_connection() else "disconnected"
    
    def enrich_company(self, domain: str) -> Dict[str, Any]:
        """Enrich company data from domain"""
        if self.mock_mode:
            return self._get_mock_company_data(domain)
        
        # In production, use Apollo API
        return {}
    
    def enrich_person(self, name: str, company: str) -> Dict[str, Any]:
        """Enrich person data"""
        if self.mock_mode:
            return self._get_mock_person_data(name, company)
        
        # In production, use Apollo API
        return {}
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for companies"""
        if self.mock_mode:
            return self._get_mock_companies(query, limit)
        
        # In production, use Apollo API
        return []
    
    def search_people(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for people"""
        if self.mock_mode:
            return self._get_mock_people(query, limit)
        
        # In production, use Apollo API
        return []
    
    def _get_mock_company_data(self, domain: str) -> Dict[str, Any]:
        """Generate mock company data"""
        company_name = domain.split('.')[0].title()
        return {
            "id": f"mock_apollo_company_{datetime.now().timestamp()}",
            "name": f"{company_name} Inc.",
            "domain": domain,
            "industry": "Technology",
            "size": "50-200 employees",
            "revenue": "$10M-$50M",
            "location": "San Francisco, CA",
            "description": f"Leading technology company in the {company_name} space",
            "technologies": ["React", "Node.js", "AWS", "PostgreSQL"],
            "social_media": {
                "linkedin": f"https://linkedin.com/company/{company_name.lower()}",
                "twitter": f"@{company_name.lower()}",
                "website": f"https://{domain}"
            },
            "funding": {
                "total_raised": "$5M",
                "last_round": "Series A",
                "investors": ["Accel", "Sequoia"]
            },
            "enriched_at": datetime.now().isoformat()
        }
    
    def _get_mock_person_data(self, name: str, company: str) -> Dict[str, Any]:
        """Generate mock person data"""
        first_name, last_name = name.split(' ', 1) if ' ' in name else (name, "Mock")
        return {
            "id": f"mock_apollo_person_{datetime.now().timestamp()}",
            "name": name,
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}@{company.lower().replace(' ', '')}.com",
            "title": "Senior Manager",
            "company": company,
            "linkedin_url": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
            "location": "San Francisco, CA",
            "bio": f"Experienced professional at {company} with expertise in technology and business development.",
            "skills": ["Leadership", "Strategy", "Technology", "Sales"],
            "experience": [
                {
                    "company": company,
                    "title": "Senior Manager",
                    "duration": "2+ years"
                }
            ],
            "enriched_at": datetime.now().isoformat()
        }
    
    def _get_mock_companies(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock company search results"""
        companies = []
        for i in range(min(limit, 5)):
            companies.append({
                "id": f"mock_apollo_company_{i}",
                "name": f"Mock Company {i}",
                "domain": f"mock{i}.com",
                "industry": "Technology",
                "size": "50-200 employees",
                "location": "San Francisco, CA"
            })
        return companies
    
    def _get_mock_people(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Generate mock people search results"""
        people = []
        for i in range(min(limit, 5)):
            people.append({
                "id": f"mock_apollo_person_{i}",
                "name": f"Mock Person {i}",
                "title": "Manager",
                "company": f"Mock Company {i}",
                "email": f"person{i}@mock{i}.com",
                "linkedin_url": f"https://linkedin.com/in/mock-person-{i}"
            })
        return people
