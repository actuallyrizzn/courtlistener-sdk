"""
Tests for Opinions Cited API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.opinions_cited import OpinionsCitedAPI


class TestOpinionsCitedAPI:
    """Test cases for Opinions Cited API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = OpinionsCitedAPI(self.mock_client)
    
    def test_list_opinions_cited(self):
        """Test listing opinions cited."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                    "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/456/"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(citing_opinion=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "opinions-cited/",
            params={"citing_opinion": 123}
        )
    
    def test_list_with_cited_opinion_filter(self):
        """Test listing with cited opinion filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(cited_opinion=456)
        
        expected_params = {"cited_opinion": 456}
        self.mock_client.get.assert_called_once_with("opinions-cited/", params=expected_params)
    
    def test_get_opinion_cited(self):
        """Test getting a specific opinion cited."""
        mock_response = {
            "id": 1,
            "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
            "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/456/"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("opinions-cited/1/")
    
    def test_paginate_opinions_cited(self):
        """Test paginating opinions cited."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(citing_opinion=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "opinions-cited/",
            params={"citing_opinion": 123}
        )
