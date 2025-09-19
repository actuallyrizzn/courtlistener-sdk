"""
Tests for NonInvestmentIncome model.
"""

import pytest
from courtlistener.models.non_investment_income import NonInvestmentIncome


class TestNonInvestmentIncome:
    """Test cases for NonInvestmentIncome model."""
    
    def test_non_investment_income_creation(self):
        """Test creating a NonInvestmentIncome instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Judicial Salary",
            "amount": 150000.0,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/non-investment-incomes/1/",
            "absolute_url": "https://www.courtlistener.com/non-investment-incomes/1/"
        }
        
        income = NonInvestmentIncome(data)
        
        assert income.id == 1
        assert income.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert income.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert income.description == "Judicial Salary"
        assert income.amount == 150000.0
        assert income.date_created == "2023-01-01T00:00:00Z"
        assert income.date_modified == "2023-01-02T00:00:00Z"
        assert income.resource_uri == "https://api.courtlistener.com/api/rest/v4/non-investment-incomes/1/"
        assert income.absolute_url == "https://www.courtlistener.com/non-investment-incomes/1/"
    
    def test_non_investment_income_with_none_values(self):
        """Test creating a NonInvestmentIncome with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "amount": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        income = NonInvestmentIncome(data)
        
        assert income.id == 1
        assert income.financial_disclosure is None
        assert income.judge is None
        assert income.description is None
        assert income.amount is None
        assert income.date_created is None
        assert income.date_modified is None
        assert income.resource_uri is None
        assert income.absolute_url is None
