"""
Tests for Reimbursements API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.reimbursements import ReimbursementsAPI


class TestReimbursementsAPI:
    """Test cases for Reimbursements API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = ReimbursementsAPI(self.mock_client)
    
    def test_list_reimbursements(self):
        """Test listing reimbursements."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
                    "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
                    "description": "Travel expenses",
                    "amount": 500.0
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(financial_disclosure=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "reimbursements/",
            params={"financial_disclosure": 123}
        )
    
    def test_list_with_judge_filter(self):
        """Test listing with judge filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(judge=456)
        
        expected_params = {"judge": 456}
        self.mock_client.get.assert_called_once_with("reimbursements/", params=expected_params)
    
    def test_get_reimbursement(self):
        """Test getting a specific reimbursement."""
        mock_response = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "description": "Travel expenses"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("reimbursements/1/")
    
    def test_paginate_reimbursements(self):
        """Test paginating reimbursements."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(financial_disclosure=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "reimbursements/",
            params={"financial_disclosure": 123}
        )
