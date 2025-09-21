"""
Tests for Debt model.
"""

import pytest
from courtlistener.models.debt import Debt


class TestDebt:
    """Test cases for Debt model."""
    
    def test_debt_creation(self):
        """Test creating a Debt instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Home mortgage",
            "amount": 250000.0,
            "creditor": "Bank of America",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/debts/1/",
            "absolute_url": "https://www.courtlistener.com/debts/1/"
        }
        
        debt = Debt(data)
        
        assert debt.id == 1
        assert debt.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert debt.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert debt.description == "Home mortgage"
        assert debt.amount == 250000.0
        assert debt.creditor == "Bank of America"
        assert debt.date_created == "2023-01-01T00:00:00Z"
        assert debt.date_modified == "2023-01-02T00:00:00Z"
        assert debt.resource_uri == "https://api.courtlistener.com/api/rest/v4/debts/1/"
        assert debt.absolute_url == "https://www.courtlistener.com/debts/1/"
    
    def test_debt_with_none_values(self):
        """Test creating a Debt with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "amount": None,
            "creditor": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        debt = Debt(data)
        
        assert debt.id == 1
        assert debt.financial_disclosure is None
        assert debt.judge is None
        assert debt.description is None
        assert debt.amount is None
        assert debt.creditor is None
        assert debt.date_created is None
        assert debt.date_modified is None
        assert debt.resource_uri is None
        assert debt.absolute_url is None
