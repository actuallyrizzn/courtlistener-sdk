"""
Tests for Investment model.
"""

import pytest
from courtlistener.models.investment import Investment


class TestInvestment:
    """Test cases for Investment model."""
    
    def test_investment_creation(self):
        """Test creating an Investment instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Apple Inc. Stock",
            "value_min": 1000.0,
            "value_max": 5000.0,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/investments/1/",
            "absolute_url": "https://www.courtlistener.com/investments/1/"
        }
        
        investment = Investment(data)
        
        assert investment.id == 1
        assert investment.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert investment.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert investment.description == "Apple Inc. Stock"
        assert investment.value_min == 1000.0
        assert investment.value_max == 5000.0
        assert investment.date_created == "2023-01-01T00:00:00Z"
        assert investment.date_modified == "2023-01-02T00:00:00Z"
        assert investment.resource_uri == "https://api.courtlistener.com/api/rest/v4/investments/1/"
        assert investment.absolute_url == "https://www.courtlistener.com/investments/1/"
    
    def test_investment_with_none_values(self):
        """Test creating an Investment with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "value_min": None,
            "value_max": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        investment = Investment(data)
        
        assert investment.id == 1
        assert investment.financial_disclosure is None
        assert investment.judge is None
        assert investment.description is None
        assert investment.value_min is None
        assert investment.value_max is None
        assert investment.date_created is None
        assert investment.date_modified is None
        assert investment.resource_uri is None
        assert investment.absolute_url is None
