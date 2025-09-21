"""
Tests for ABA Ratings API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.aba_ratings import ABARatingsAPI


class TestABARatingsAPI:
    """Test cases for ABA Ratings API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = ABARatingsAPI(self.mock_client)
    
    def test_list_aba_ratings(self):
        """Test listing ABA ratings."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "rating": "Well Qualified",
                    "year": 2020
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(person=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "aba-ratings/",
            params={"person": 123}
        )
    
    def test_list_without_filters(self):
        """Test listing without filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        expected_params = {}
        self.mock_client.get.assert_called_once_with("aba-ratings/", params=expected_params)
    
    def test_get_aba_rating(self):
        """Test getting a specific ABA rating."""
        mock_response = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "rating": "Well Qualified"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("aba-ratings/1/")
    
    def test_paginate_aba_ratings(self):
        """Test paginating ABA ratings."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(person=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "aba-ratings/",
            params={"person": 123}
        )
