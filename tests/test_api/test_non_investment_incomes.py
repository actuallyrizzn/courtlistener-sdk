"""
Tests for Non-Investment Incomes API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.non_investment_incomes import NonInvestmentIncomesAPI


class TestNonInvestmentIncomesAPI:
    """Test cases for Non-Investment Incomes API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = NonInvestmentIncomesAPI(self.mock_client)
    
    def test_list_non_investment_incomes(self):
        """Test listing non-investment incomes."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
                    "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
                    "description": "Salary",
                    "amount": 150000.0
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(financial_disclosure=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "non-investment-incomes/",
            params={"financial_disclosure": 123}
        )
    
    def test_list_with_judge_filter(self):
        """Test listing with judge filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(judge=456)
        
        expected_params = {"judge": 456}
        self.mock_client.get.assert_called_once_with("non-investment-incomes/", params=expected_params)
    
    def test_get_non_investment_income(self):
        """Test getting a specific non-investment income."""
        mock_response = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "description": "Salary"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("non-investment-incomes/1/")
    
    def test_paginate_non_investment_incomes(self):
        """Test paginating non-investment incomes."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(financial_disclosure=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "non-investment-incomes/",
            params={"financial_disclosure": 123}
        )
