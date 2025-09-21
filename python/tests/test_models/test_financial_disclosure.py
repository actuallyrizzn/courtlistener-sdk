"""
Tests for FinancialDisclosure model.
"""

import pytest
from courtlistener.models.financial_disclosure import FinancialDisclosure


class TestFinancialDisclosure:
    """Test cases for FinancialDisclosure model."""
    
    def test_financial_disclosure_creation(self):
        """Test creating a FinancialDisclosure instance."""
        data = {
            "id": 1,
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/123/",
            "year": 2023,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/1/",
            "absolute_url": "https://www.courtlistener.com/financial-disclosures/1/"
        }
        
        disclosure = FinancialDisclosure(data)
        
        assert disclosure.id == 1
        assert disclosure.judge == "https://api.courtlistener.com/api/rest/v4/judges/123/"
        assert disclosure.year == 2023
        assert disclosure.date_created == "2023-01-01T00:00:00Z"
        assert disclosure.date_modified == "2023-01-02T00:00:00Z"
        assert disclosure.resource_uri == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/1/"
        assert disclosure.absolute_url == "https://www.courtlistener.com/financial-disclosures/1/"
    
    def test_financial_disclosure_with_none_values(self):
        """Test creating a FinancialDisclosure with None values."""
        data = {
            "id": 1,
            "judge": None,
            "year": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        disclosure = FinancialDisclosure(data)
        
        assert disclosure.id == 1
        assert disclosure.judge is None
        assert disclosure.year is None
        assert disclosure.date_created is None
        assert disclosure.date_modified is None
        assert disclosure.resource_uri is None
        assert disclosure.absolute_url is None
