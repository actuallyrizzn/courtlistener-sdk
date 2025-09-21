"""
Tests for Financial Disclosures API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.financial_disclosures import FinancialDisclosuresAPI


class TestFinancialDisclosuresAPI:
    """Test cases for Financial Disclosures API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = FinancialDisclosuresAPI(self.mock_client)
    
    def test_list_financial_disclosures(self):
        """Test listing financial disclosures."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "judge": "https://api.courtlistener.com/api/rest/v4/judges/123/",
                    "year": 2023
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(judge=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "financial-disclosures/",
            params={"judge": 123}
        )
    
    def test_list_financial_disclosures_with_year(self):
        """Test listing financial disclosures with year filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(judge=123, year=2023)
        
        expected_params = {"judge": 123, "year": 2023}
        self.mock_client.get.assert_called_once_with(
            "financial-disclosures/",
            params=expected_params
        )
    
    def test_get_financial_disclosure(self):
        """Test getting a specific financial disclosure."""
        mock_response = {
            "id": 1,
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/123/",
            "year": 2023
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("financial-disclosures/1/")
    
    def test_paginate_financial_disclosures(self):
        """Test paginating financial disclosures."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(judge=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "financial-disclosures/",
            params={"judge": 123}
        )
