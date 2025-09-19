"""
Tests for RECAP Fetch API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.recap_fetch import RecapFetchAPI


class TestRecapFetchAPI:
    """Test cases for RECAP Fetch API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = RecapFetchAPI(self.mock_client)
    
    def test_list_recap_fetch(self):
        """Test listing RECAP fetch operations."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                    "status": "completed"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("recap-fetch/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("recap-fetch/", params=expected_params)
    
    def test_get_recap_fetch(self):
        """Test getting a specific RECAP fetch operation."""
        mock_response = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "status": "completed"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("recap-fetch/1/")
    
    def test_paginate_recap_fetch(self):
        """Test paginating RECAP fetch operations."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("recap-fetch/", params={})
