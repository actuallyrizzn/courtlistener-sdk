"""
Tests for Schools API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.schools import SchoolsAPI


class TestSchoolsAPI:
    """Test cases for Schools API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SchoolsAPI(self.mock_client)
    
    def test_list_schools(self):
        """Test listing schools."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Harvard Law School",
                    "type": "Law School",
                    "location": "Cambridge, MA"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("schools/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("schools/", params=expected_params)
    
    def test_get_school(self):
        """Test getting a specific school."""
        mock_response = {
            "id": 1,
            "name": "Harvard Law School",
            "type": "Law School"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("schools/1/")
    
    def test_paginate_schools(self):
        """Test paginating schools."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("schools/", params={})
