"""
Integration tests for RECAP-related endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestRecapIntegration:
    """Integration tests for RECAP endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_recap_documents_workflow(self):
        """Test RECAP documents workflow."""
        # Mock RECAP documents list
        mock_documents = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                    "file_url": "https://example.com/doc1.pdf",
                    "file_size": 1024,
                    "file_type": "pdf"
                },
                {
                    "id": 2,
                    "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                    "file_url": "https://example.com/doc2.pdf",
                    "file_size": 2048,
                    "file_type": "pdf"
                }
            ]
        }
        self.client.get.return_value = mock_documents
        
        # Test getting RECAP documents
        documents = self.client.recap_documents.list(docket=123)
        assert documents["count"] == 2
        assert len(documents["results"]) == 2
        
        # Test getting specific document
        mock_document = mock_documents["results"][0]
        self.client.get.return_value = mock_document
        
        document = self.client.recap_documents.get(1)
        assert document["id"] == 1
        assert document["file_type"] == "pdf"
    
    def test_recap_fetch_workflow(self):
        """Test RECAP fetch operations workflow."""
        # Mock RECAP fetch operations
        mock_fetches = {
            "count": 1,
            "results": [{
                "id": 1,
                "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                "status": "completed"
            }]
        }
        self.client.get.return_value = mock_fetches
        
        # Test getting RECAP fetch operations
        fetches = self.client.recap_fetch.list()
        assert fetches["count"] == 1
        assert len(fetches["results"]) == 1
        
        # Test getting specific fetch operation
        mock_fetch = mock_fetches["results"][0]
        self.client.get.return_value = mock_fetch
        
        fetch = self.client.recap_fetch.get(1)
        assert fetch["status"] == "completed"
    
    def test_recap_query_workflow(self):
        """Test RECAP query operations workflow."""
        # Mock RECAP query operations
        mock_queries = {
            "count": 1,
            "results": [{
                "id": 1,
                "query": "constitutional law",
                "status": "completed"
            }]
        }
        self.client.get.return_value = mock_queries
        
        # Test getting RECAP query operations
        queries = self.client.recap_query.list()
        assert queries["count"] == 1
        assert len(queries["results"]) == 1
        
        # Test getting specific query operation
        mock_query = mock_queries["results"][0]
        self.client.get.return_value = mock_query
        
        query = self.client.recap_query.get(1)
        assert query["query"] == "constitutional law"
    
    def test_recap_endpoints_pagination(self):
        """Test that pagination works for RECAP endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        recap_endpoints = [
            'recap_documents',
            'recap_fetch',
            'recap_query'
        ]
        
        for endpoint_name in recap_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.paginate()
            assert result == mock_iterator
    
    def test_recap_documents_filtering(self):
        """Test RECAP documents filtering."""
        mock_response = {"count": 0, "results": []}
        self.client.get.return_value = mock_response
        
        # Test filtering by docket
        self.client.recap_documents.list(docket=123)
        self.client.get.assert_called_with("recap-documents/", params={"docket": 123})
        
        # Test filtering by docket entry
        self.client.recap_documents.list(docket_entry=456)
        self.client.get.assert_called_with("recap-documents/", params={"docket_entry": 456})
        
        # Test filtering by court
        self.client.recap_documents.list(court="scotus")
        self.client.get.assert_called_with("recap-documents/", params={"court": "scotus"})
    
    def test_recap_get_methods(self):
        """Test that get methods work for all RECAP endpoints."""
        mock_response = {"id": 1, "status": "completed"}
        self.client.get.return_value = mock_response
        
        recap_endpoints = [
            'recap_documents',
            'recap_fetch',
            'recap_query'
        ]
        
        for endpoint_name in recap_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.get(1)
            assert result == mock_response
