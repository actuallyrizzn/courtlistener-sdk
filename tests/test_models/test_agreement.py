"""
Tests for Agreement model.
"""

import pytest
from courtlistener.models.agreement import Agreement


class TestAgreement:
    """Test cases for Agreement model."""
    
    def test_agreement_creation(self):
        """Test creating an Agreement instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Consulting agreement with law firm",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/agreements/1/",
            "absolute_url": "https://www.courtlistener.com/agreements/1/"
        }
        
        agreement = Agreement(data)
        
        assert agreement.id == 1
        assert agreement.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert agreement.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert agreement.description == "Consulting agreement with law firm"
        assert agreement.date_created == "2023-01-01T00:00:00Z"
        assert agreement.date_modified == "2023-01-02T00:00:00Z"
        assert agreement.resource_uri == "https://api.courtlistener.com/api/rest/v4/agreements/1/"
        assert agreement.absolute_url == "https://www.courtlistener.com/agreements/1/"
    
    def test_agreement_with_none_values(self):
        """Test creating an Agreement with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        agreement = Agreement(data)
        
        assert agreement.id == 1
        assert agreement.financial_disclosure is None
        assert agreement.judge is None
        assert agreement.description is None
        assert agreement.date_created is None
        assert agreement.date_modified is None
        assert agreement.resource_uri is None
        assert agreement.absolute_url is None
