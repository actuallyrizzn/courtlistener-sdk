"""
Tests for Retention Events API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.retention_events import RetentionEventsAPI


class TestRetentionEventsAPI:
    """Test cases for Retention Events API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = RetentionEventsAPI(self.mock_client)
    
    def test_list_retention_events(self):
        """Test listing retention events."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "event_type": "Document Deletion",
                    "description": "Documents older than 10 years deleted",
                    "date": "2023-01-01"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("retention-events/", params={})
    
    def test_list_with_params(self):
        """Test listing with parameters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(page=2, page_size=50)
        
        expected_params = {"page": 2, "page_size": 50}
        self.mock_client.get.assert_called_once_with("retention-events/", params=expected_params)
    
    def test_get_retention_event(self):
        """Test getting a specific retention event."""
        mock_response = {
            "id": 1,
            "event_type": "Document Deletion",
            "description": "Documents older than 10 years deleted"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("retention-events/1/")
    
    def test_paginate_retention_events(self):
        """Test paginating retention events."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate()
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with("retention-events/", params={})
