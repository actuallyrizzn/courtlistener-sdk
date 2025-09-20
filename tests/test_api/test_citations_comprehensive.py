"""
Comprehensive tests for Citations API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.citations import CitationsAPI, Citation
from courtlistener.exceptions import ValidationError, CourtListenerError


class TestCitationsAPIComprehensive:
    """Comprehensive tests for CitationsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = CitationsAPI(self.mock_client)
    
    def test_init(self):
        """Test CitationsAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "citations/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Citation
    
    def test_get_citations_by_opinion_success(self):
        """Test get_citations_by_opinion with valid opinion ID."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.citations.validate_id') as mock_validate:
            result = self.api.get_citations_by_opinion(1)
            
            assert result == mock_response
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("opinions-cited/", params={"citing_opinion": 1})
    
    def test_get_citations_by_opinion_invalid_id(self):
        """Test get_citations_by_opinion with invalid opinion ID."""
        with patch('courtlistener.api.citations.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_citations_by_opinion(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_citations_by_opinion_error(self):
        """Test get_citations_by_opinion with API error."""
        with patch('courtlistener.api.citations.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("API Error")
            
            with pytest.raises(CourtListenerError):
                self.api.get_citations_by_opinion(1)
    
    def test_get_cited_by_opinions_success(self):
        """Test get_cited_by_opinions with valid opinion ID."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.citations.validate_id') as mock_validate:
            result = self.api.get_cited_by_opinions(1)
            
            assert result == mock_response
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("opinions-cited/", params={"cited_opinion": 1})
    
    def test_get_cited_by_opinions_invalid_id(self):
        """Test get_cited_by_opinions with invalid opinion ID."""
        with patch('courtlistener.api.citations.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_cited_by_opinions(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_cited_by_opinions_error(self):
        """Test get_cited_by_opinions with API error."""
        with patch('courtlistener.api.citations.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("API Error")
            
            with pytest.raises(CourtListenerError):
                self.api.get_cited_by_opinions(1)
    
    def test_lookup_citations_success(self):
        """Test lookup_citations with valid text."""
        mock_response = [{"citation": "410 U.S. 113", "matched_text": "Roe v. Wade"}]
        self.mock_client.post.return_value = mock_response
        
        result = self.api.lookup_citations("Roe v. Wade, 410 U.S. 113 (1973)")
        
        assert result == mock_response
        expected_data = {"text": "Roe v. Wade, 410 U.S. 113 (1973)"}
        self.mock_client.post.assert_called_once_with("citation-lookup/", json_data=expected_data)
    
    def test_lookup_citations_empty_text(self):
        """Test lookup_citations with empty text."""
        mock_response = []
        self.mock_client.post.return_value = mock_response
        
        result = self.api.lookup_citations("")
        
        assert result == mock_response
        expected_data = {"text": ""}
        self.mock_client.post.assert_called_once_with("citation-lookup/", json_data=expected_data)
    
    def test_lookup_citations_error(self):
        """Test lookup_citations with API error."""
        self.mock_client.post.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.lookup_citations("test text")
    
    def test_list_citations_basic(self):
        """Test basic list_citations functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_citations()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 1})
    
    def test_list_citations_with_page(self):
        """Test list_citations with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_citations(page=2)
        
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 2})
    
    def test_list_citations_with_filters(self):
        """Test list_citations with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"citing_opinion": 1, "cited_opinion": 2}
        self.api.list_citations(page=1, **filters)
        
        expected_params = {"page": 1, "citing_opinion": 1, "cited_opinion": 2}
        self.mock_client.get.assert_called_once_with("citations/", params=expected_params)
    
    def test_list_citations_no_filters(self):
        """Test list_citations with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_citations(page=1)
        
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 1})
    
    def test_search_citations_basic(self):
        """Test basic search_citations functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_citations()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 1})
    
    def test_search_citations_with_page(self):
        """Test search_citations with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_citations(page=2)
        
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 2})
    
    def test_search_citations_with_filters(self):
        """Test search_citations with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"citing_opinion": 1, "cited_opinion": 2}
        self.api.search_citations(page=1, **filters)
        
        expected_params = {"page": 1, "citing_opinion": 1, "cited_opinion": 2}
        self.mock_client.get.assert_called_once_with("citations/", params=expected_params)
    
    def test_search_citations_no_filters(self):
        """Test search_citations with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_citations(page=1)
        
        self.mock_client.get.assert_called_once_with("citations/", params={"page": 1})
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_citations()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.post.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.lookup_citations("test text")
