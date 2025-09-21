"""
Integration tests for Citations and Legal Research endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestCitationsIntegration:
    """Integration tests for citations endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_opinions_cited_workflow(self):
        """Test opinions cited workflow."""
        # Mock opinions cited list
        mock_citations = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                    "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/456/"
                },
                {
                    "id": 2,
                    "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                    "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/789/"
                }
            ]
        }
        self.client.get.return_value = mock_citations
        
        # Test getting opinions cited by a specific opinion
        citations = self.client.opinions_cited.list(citing_opinion=123)
        assert citations["count"] == 2
        assert len(citations["results"]) == 2
        
        # Test getting opinions that cite a specific opinion
        citations = self.client.opinions_cited.list(cited_opinion=456)
        assert citations["count"] == 2
        assert len(citations["results"]) == 2
        
        # Test getting specific citation
        mock_citation = mock_citations["results"][0]
        self.client.get.return_value = mock_citation
        
        citation = self.client.opinions_cited.get(1)
        assert citation["id"] == 1
        assert "citing_opinion" in citation
        assert "cited_opinion" in citation
    
    def test_citations_workflow(self):
        """Test citations workflow."""
        # Mock citations list
        mock_citations = {
            "count": 1,
            "results": [{
                "id": 1,
                "opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                "citation_text": "123 U.S. 456 (2023)"
            }]
        }
        self.client.get.return_value = mock_citations
        
        # Test getting citations
        citations = self.client.citations.list()
        assert citations["count"] == 1
        assert len(citations["results"]) == 1
        
        # Test getting specific citation
        mock_citation = mock_citations["results"][0]
        self.client.get.return_value = mock_citation
        
        citation = self.client.citations.get(1)
        assert citation["citation_text"] == "123 U.S. 456 (2023)"
    
    def test_citations_pagination(self):
        """Test that pagination works for citations endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        citations_endpoints = [
            'opinions_cited',
            'citations'
        ]
        
        for endpoint_name in citations_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.paginate()
            assert result == mock_iterator
    
    def test_opinions_cited_filtering(self):
        """Test opinions cited filtering."""
        mock_response = {"count": 0, "results": []}
        self.client.get.return_value = mock_response
        
        # Test filtering by citing opinion
        self.client.opinions_cited.list(citing_opinion=123)
        self.client.get.assert_called_with("opinions-cited/", params={"citing_opinion": 123})
        
        # Test filtering by cited opinion
        self.client.opinions_cited.list(cited_opinion=456)
        self.client.get.assert_called_with("opinions-cited/", params={"cited_opinion": 456})
    
    def test_citations_get_methods(self):
        """Test that get methods work for all citations endpoints."""
        mock_response = {"id": 1, "citation_text": "123 U.S. 456 (2023)"}
        self.client.get.return_value = mock_response
        
        citations_endpoints = [
            'opinions_cited',
            'citations'
        ]
        
        for endpoint_name in citations_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.get(1)
            assert result == mock_response
