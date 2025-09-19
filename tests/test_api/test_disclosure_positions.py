"""
Tests for Disclosure Positions API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.disclosure_positions import DisclosurePositionsAPI


class TestDisclosurePositionsAPI:
    """Test cases for Disclosure Positions API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = DisclosurePositionsAPI(self.mock_client)
    
    def test_list_disclosure_positions(self):
        """Test listing disclosure positions."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
                    "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
                    "position": "Board Member",
                    "organization": "Legal Foundation"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(financial_disclosure=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "disclosure-positions/",
            params={"financial_disclosure": 123}
        )
    
    def test_list_with_judge_filter(self):
        """Test listing with judge filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(judge=456)
        
        expected_params = {"judge": 456}
        self.mock_client.get.assert_called_once_with("disclosure-positions/", params=expected_params)
    
    def test_get_disclosure_position(self):
        """Test getting a specific disclosure position."""
        mock_response = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "position": "Board Member"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("disclosure-positions/1/")
    
    def test_paginate_disclosure_positions(self):
        """Test paginating disclosure positions."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(financial_disclosure=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "disclosure-positions/",
            params={"financial_disclosure": 123}
        )
