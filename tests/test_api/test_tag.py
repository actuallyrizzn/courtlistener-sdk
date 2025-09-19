"""
Tests for Tag API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.tag import TagAPI


class TestTagAPI:
    """Test cases for Tag API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = TagAPI(self.mock_client)
    
    def test_list_tags(self):
        """Test listing tags."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Constitutional Law",
                    "description": "Cases involving constitutional issues"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("tag/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("tag/", params=expected_params)
    
    def test_get_tag(self):
        """Test getting a specific tag."""
        mock_response = {
            "id": 1,
            "name": "Constitutional Law",
            "description": "Cases involving constitutional issues"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("tag/1/")
    
    def test_paginate_tags(self):
        """Test paginating tags."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("tag/", params={})
