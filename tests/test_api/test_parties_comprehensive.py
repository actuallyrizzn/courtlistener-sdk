"""
Comprehensive tests for Parties API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.parties import PartiesAPI, Party
from courtlistener.exceptions import ValidationError, CourtListenerError


class TestPartiesAPIComprehensive:
    """Comprehensive tests for PartiesAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = PartiesAPI(self.mock_client)
    
    def test_init(self):
        """Test PartiesAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "parties/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Party
    
    def test_list_parties_basic(self):
        """Test basic list_parties functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_parties()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("parties/", params={"page": 1})
    
    def test_list_parties_with_page(self):
        """Test list_parties with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_parties(page=2)
        
        self.mock_client.get.assert_called_once_with("parties/", params={"page": 2})
    
    def test_list_parties_with_query(self):
        """Test list_parties with search query."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_parties(q="plaintiff")
        
        self.mock_client.get.assert_called_once_with("parties/", params={"page": 1, "q": "plaintiff"})
    
    def test_list_parties_with_filters(self):
        """Test list_parties with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"party_type": "plaintiff", "docket": 1}
        self.api.list_parties(page=1, **filters)
        
        expected_params = {"page": 1, "party_type": "plaintiff", "docket": 1}
        self.mock_client.get.assert_called_once_with("parties/", params=expected_params)
    
    def test_list_parties_with_query_and_filters(self):
        """Test list_parties with both query and filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"party_type": "plaintiff"}
        self.api.list_parties(q="smith", page=2, **filters)
        
        expected_params = {"page": 2, "q": "smith", "party_type": "plaintiff"}
        self.mock_client.get.assert_called_once_with("parties/", params=expected_params)
    
    def test_list_parties_no_filters(self):
        """Test list_parties with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_parties(page=1)
        
        self.mock_client.get.assert_called_once_with("parties/", params={"page": 1})
    
    def test_get_party_success(self):
        """Test get_party with valid party ID."""
        mock_response = {"id": 1, "name": "John Smith", "party_type": "plaintiff"}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.parties.validate_id') as mock_validate:
            result = self.api.get_party(1)
            
            assert isinstance(result, Party)
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("parties/1/")
    
    def test_get_party_invalid_id(self):
        """Test get_party with invalid party ID."""
        with patch('courtlistener.api.parties.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_party(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_party_not_found(self):
        """Test get_party with non-existent party ID."""
        with patch('courtlistener.api.parties.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("Party not found")
            
            with pytest.raises(CourtListenerError):
                self.api.get_party(999)
    
    def test_search_parties_basic(self):
        """Test search_parties without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_parties("plaintiff")
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("parties/", params={"q": "plaintiff", "page": 1})
    
    def test_search_parties_with_page(self):
        """Test search_parties with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_parties("plaintiff", page=2)
        
        self.mock_client.get.assert_called_once_with("parties/", params={"q": "plaintiff", "page": 2})
    
    def test_search_parties_with_filters(self):
        """Test search_parties with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"party_type": "plaintiff", "docket": 1}
        self.api.search_parties("smith", page=1, **filters)
        
        expected_params = {"q": "smith", "page": 1, "party_type": "plaintiff", "docket": 1}
        self.mock_client.get.assert_called_once_with("parties/", params=expected_params)
    
    def test_search_parties_no_filters(self):
        """Test search_parties with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_parties("plaintiff", page=1)
        
        self.mock_client.get.assert_called_once_with("parties/", params={"q": "plaintiff", "page": 1})
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_parties()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.search_parties("plaintiff")
