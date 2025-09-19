"""
Tests for Originating Court Information API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.originating_court_information import OriginatingCourtInformationAPI


class TestOriginatingCourtInformationAPI:
    """Test cases for Originating Court Information API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = OriginatingCourtInformationAPI(self.mock_client)
    
    def test_list_originating_court_information(self):
        """Test listing originating court information."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
                    "jurisdiction": "Federal",
                    "description": "Supreme Court of the United States"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("originating-court-information/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("originating-court-information/", params=expected_params)
    
    def test_get_originating_court_information(self):
        """Test getting specific originating court information."""
        mock_response = {
            "id": 1,
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "jurisdiction": "Federal"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("originating-court-information/1/")
    
    def test_paginate_originating_court_information(self):
        """Test paginating originating court information."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("originating-court-information/", params={})
