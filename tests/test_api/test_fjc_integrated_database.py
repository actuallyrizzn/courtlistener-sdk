"""
Tests for FJC Integrated Database API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.fjc_integrated_database import FJCIntegratedDatabaseAPI


class TestFJCIntegratedDatabaseAPI:
    """Test cases for FJC Integrated Database API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = FJCIntegratedDatabaseAPI(self.mock_client)
    
    def test_list_fjc_integrated_database(self):
        """Test listing FJC integrated database records."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
                    "position": "Justice"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("fjc-integrated-database/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("fjc-integrated-database/", params=expected_params)
    
    def test_get_fjc_integrated_database(self):
        """Test getting specific FJC integrated database record."""
        mock_response = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("fjc-integrated-database/1/")
    
    def test_paginate_fjc_integrated_database(self):
        """Test paginating FJC integrated database records."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("fjc-integrated-database/", params={})
