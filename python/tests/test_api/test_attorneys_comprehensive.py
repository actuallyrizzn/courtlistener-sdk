"""
Comprehensive tests for Attorneys API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.attorneys import AttorneysAPI, Attorney
from courtlistener.exceptions import ValidationError, CourtListenerError


class TestAttorneysAPIComprehensive:
    """Comprehensive tests for AttorneysAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = AttorneysAPI(self.mock_client)
    
    def test_init(self):
        """Test AttorneysAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "attorneys/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Attorney
    
    def test_list_attorneys_basic(self):
        """Test basic list_attorneys functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_attorneys()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("attorneys/", params={"page": 1})
    
    def test_list_attorneys_with_page(self):
        """Test list_attorneys with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_attorneys(page=2)
        
        self.mock_client.get.assert_called_once_with("attorneys/", params={"page": 2})
    
    def test_list_attorneys_with_query(self):
        """Test list_attorneys with search query."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_attorneys(q="smith")
        
        self.mock_client.get.assert_called_once_with("attorneys/", params={"page": 1, "q": "smith"})
    
    def test_list_attorneys_with_filters(self):
        """Test list_attorneys with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"firm": "Test Firm", "state": "CA"}
        self.api.list_attorneys(page=1, **filters)
        
        expected_params = {"page": 1, "firm": "Test Firm", "state": "CA"}
        self.mock_client.get.assert_called_once_with("attorneys/", params=expected_params)
    
    def test_list_attorneys_with_query_and_filters(self):
        """Test list_attorneys with both query and filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"firm": "Test Firm"}
        self.api.list_attorneys(q="smith", page=2, **filters)
        
        expected_params = {"page": 2, "q": "smith", "firm": "Test Firm"}
        self.mock_client.get.assert_called_once_with("attorneys/", params=expected_params)
    
    def test_list_attorneys_no_filters(self):
        """Test list_attorneys with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_attorneys(page=1)
        
        self.mock_client.get.assert_called_once_with("attorneys/", params={"page": 1})
    
    def test_get_attorney_success(self):
        """Test get_attorney with valid attorney ID."""
        mock_response = {"id": 1, "name": "John Smith", "firm": "Test Firm"}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.attorneys.validate_id') as mock_validate:
            result = self.api.get_attorney(1)
            
            assert isinstance(result, Attorney)
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("attorneys/1/")
    
    def test_get_attorney_invalid_id(self):
        """Test get_attorney with invalid attorney ID."""
        with patch('courtlistener.api.attorneys.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_attorney(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_attorney_not_found(self):
        """Test get_attorney with non-existent attorney ID."""
        with patch('courtlistener.api.attorneys.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("Attorney not found")
            
            with pytest.raises(CourtListenerError):
                self.api.get_attorney(999)
    
    def test_search_attorneys_basic(self):
        """Test search_attorneys without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_attorneys("smith")
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("attorneys/", params={"q": "smith", "page": 1})
    
    def test_search_attorneys_with_page(self):
        """Test search_attorneys with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_attorneys("smith", page=2)
        
        self.mock_client.get.assert_called_once_with("attorneys/", params={"q": "smith", "page": 2})
    
    def test_search_attorneys_with_filters(self):
        """Test search_attorneys with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"firm": "Test Firm", "state": "CA"}
        self.api.search_attorneys("smith", page=1, **filters)
        
        expected_params = {"q": "smith", "page": 1, "firm": "Test Firm", "state": "CA"}
        self.mock_client.get.assert_called_once_with("attorneys/", params=expected_params)
    
    def test_search_attorneys_no_filters(self):
        """Test search_attorneys with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_attorneys("smith", page=1)
        
        self.mock_client.get.assert_called_once_with("attorneys/", params={"q": "smith", "page": 1})
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_attorneys()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.search_attorneys("smith")
