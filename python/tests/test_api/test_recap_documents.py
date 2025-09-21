"""
Tests for RECAP Documents API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.recap_documents import RecapDocumentsAPI


class TestRecapDocumentsAPI:
    """Test cases for RECAP Documents API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = RecapDocumentsAPI(self.mock_client)
    
    def test_list_recap_documents(self):
        """Test listing RECAP documents."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                    "file_url": "https://example.com/document.pdf",
                    "file_size": 1024,
                    "file_type": "pdf"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(docket=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "recap-documents/",
            params={"docket": 123}
        )
    
    def test_list_recap_documents_with_filters(self):
        """Test listing RECAP documents with multiple filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(
            docket=123,
            docket_entry=456,
            court="scotus"
        )
        
        expected_params = {
            "docket": 123,
            "docket_entry": 456,
            "court": "scotus"
        }
        self.mock_client.get.assert_called_once_with(
            "recap-documents/",
            params=expected_params
        )
    
    def test_get_recap_document(self):
        """Test getting a specific RECAP document."""
        mock_response = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "file_url": "https://example.com/document.pdf"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("recap-documents/1/")
    
    def test_paginate_recap_documents(self):
        """Test paginating RECAP documents."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(docket=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "recap-documents/",
            params={"docket": 123}
        )
