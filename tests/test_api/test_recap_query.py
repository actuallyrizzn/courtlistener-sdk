"""
Tests for RECAP Query API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.recap_query import RecapQueryAPI


class TestRecapQueryAPI:
    """Test cases for RECAP Query API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = RecapQueryAPI(self.mock_client)
    
    def test_list_recap_query(self):
        """Test listing RECAP query operations."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "query": "constitutional law",
                    "status": "completed"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("recap-query/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("recap-query/", params=expected_params)
    
    def test_get_recap_query(self):
        """Test getting a specific RECAP query operation."""
        mock_response = {
            "id": 1,
            "query": "constitutional law",
            "status": "completed"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("recap-query/1/")
    
    def test_paginate_recap_query(self):
        """Test paginating RECAP query operations."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("recap-query/", params={})
