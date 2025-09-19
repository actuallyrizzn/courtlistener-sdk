"""
Tests for Political Affiliations API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.political_affiliations import PoliticalAffiliationsAPI


class TestPoliticalAffiliationsAPI:
    """Test cases for Political Affiliations API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = PoliticalAffiliationsAPI(self.mock_client)
    
    def test_list_political_affiliations(self):
        """Test listing political affiliations."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "party": "Republican",
                    "year": 2020
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(person=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "political-affiliations/",
            params={"person": 123}
        )
    
    def test_list_without_filters(self):
        """Test listing without filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        expected_params = {}
        self.mock_client.get.assert_called_once_with("political-affiliations/", params=expected_params)
    
    def test_get_political_affiliation(self):
        """Test getting a specific political affiliation."""
        mock_response = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "party": "Republican"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("political-affiliations/1/")
    
    def test_paginate_political_affiliations(self):
        """Test paginating political affiliations."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(person=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "political-affiliations/",
            params={"person": 123}
        )
