"""
Comprehensive tests for Courts API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.courts import CourtsAPI
from courtlistener.models.court import Court
from courtlistener.exceptions import NotFoundError, APIError


class TestCourtsAPIComprehensive:
    """Comprehensive tests for CourtsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = CourtsAPI(self.mock_client)
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "courts/"
    
    def test_list_courts_basic(self):
        """Test basic list_courts functionality."""
        mock_response = {
            "results": [
                {"id": "scotus", "name": "Supreme Court"},
                {"id": "ca1", "name": "First Circuit"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_courts()
        
        assert len(result) == 2
        assert all(isinstance(c, Court) for c in result)
        self.mock_client.get.assert_called_once_with("courts/", params={"page": 1})
    
    def test_list_courts_with_page(self):
        """Test list_courts with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_courts(page=2)
        
        self.mock_client.get.assert_called_once_with("courts/", params={"page": 2})
    
    def test_list_courts_with_query(self):
        """Test list_courts with search query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_courts(q="supreme")
        
        self.mock_client.get.assert_called_once_with("courts/", params={"page": 1, "q": "supreme"})
    
    def test_list_courts_with_filters(self):
        """Test list_courts with filters parameter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"jurisdiction": "F", "is_active": True}
        self.api.list_courts(page=1, filters=filters)
        
        expected_params = {"page": 1, "jurisdiction": "F", "is_active": True}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_list_courts_with_kwargs(self):
        """Test list_courts with additional kwargs."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_courts(page=1, jurisdiction="F", is_active=True)
        
        expected_params = {"page": 1, "jurisdiction": "F", "is_active": True}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_list_courts_with_filters_and_kwargs(self):
        """Test list_courts with both filters and kwargs."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"jurisdiction": "F"}
        self.api.list_courts(page=1, filters=filters, is_active=True)
        
        expected_params = {"page": 1, "jurisdiction": "F", "is_active": True}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_list_courts_empty_results(self):
        """Test list_courts with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_courts()
        
        assert result == []
    
    def test_list_courts_no_results_key(self):
        """Test list_courts when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_courts()
        
        assert result == []
    
    def test_get_court_success(self):
        """Test get_court with valid court ID."""
        mock_response = {"id": "scotus", "name": "Supreme Court"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court("scotus")
        
        assert isinstance(result, Court)
        self.mock_client.get.assert_called_once_with("courts/scotus/")
    
    def test_get_court_not_found(self):
        """Test get_court with non-existent court ID."""
        self.mock_client.get.side_effect = NotFoundError("Court not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_court("nonexistent")
    
    def test_search_courts(self):
        """Test search_courts method."""
        mock_response = {"results": [{"id": "scotus", "name": "Supreme Court"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_courts("supreme", page=2, jurisdiction="F")
        
        assert len(result) == 1
        expected_params = {"page": 2, "q": "supreme", "jurisdiction": "F"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_federal_courts(self):
        """Test get_federal_courts method."""
        mock_response = {"results": [{"id": "scotus", "name": "Supreme Court"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_federal_courts(page=2)
        
        assert len(result) == 1
        expected_params = {"page": 2, "jurisdiction": "F"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_federal_courts_default_page(self):
        """Test get_federal_courts with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_federal_courts()
        
        expected_params = {"page": 1, "jurisdiction": "F"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_state_courts(self):
        """Test get_state_courts method."""
        mock_response = {"results": [{"id": "ca1", "name": "First Circuit"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_state_courts(page=2)
        
        assert len(result) == 1
        expected_params = {"page": 2, "jurisdiction": "S"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_state_courts_default_page(self):
        """Test get_state_courts with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_state_courts()
        
        expected_params = {"page": 1, "jurisdiction": "S"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_court_by_url_basic(self):
        """Test get_court_by_url with basic URL."""
        mock_response = {"id": "scotus", "name": "Supreme Court"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_by_url("https://api.courtlistener.com/api/rest/v4/courts/scotus/")
        
        assert isinstance(result, Court)
        self.mock_client.get.assert_called_once_with("courts/scotus/")
    
    def test_get_court_by_url_with_trailing_slash(self):
        """Test get_court_by_url with trailing slash."""
        mock_response = {"id": "scotus", "name": "Supreme Court"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_by_url("https://api.courtlistener.com/api/rest/v4/courts/scotus/")
        
        assert isinstance(result, Court)
        self.mock_client.get.assert_called_once_with("courts/scotus/")
    
    def test_get_court_by_url_without_trailing_slash(self):
        """Test get_court_by_url without trailing slash."""
        mock_response = {"id": "scotus", "name": "Supreme Court"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_by_url("https://api.courtlistener.com/api/rest/v4/courts/scotus")
        
        assert isinstance(result, Court)
        self.mock_client.get.assert_called_once_with("courts/scotus/")
    
    def test_get_court_by_url_simple_path(self):
        """Test get_court_by_url with simple path."""
        mock_response = {"id": "scotus", "name": "Supreme Court"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_by_url("courts/scotus/")
        
        assert isinstance(result, Court)
        self.mock_client.get.assert_called_once_with("courts/scotus/")
    
    def test_get_court_opinions(self):
        """Test get_court_opinions method."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_opinions("scotus", page=2, date_filed="2023-01-01")
        
        assert result == mock_response
        expected_params = {"court": "scotus", "page": 2, "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("opinions/", params=expected_params)
    
    def test_get_court_opinions_default_page(self):
        """Test get_court_opinions with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_opinions("scotus")
        
        assert result == mock_response
        expected_params = {"court": "scotus", "page": 1}
        self.mock_client.get.assert_called_once_with("opinions/", params=expected_params)
    
    def test_get_court_dockets(self):
        """Test get_court_dockets method."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_dockets("scotus", page=2)
        
        assert result == mock_response
        expected_params = {"court": "scotus", "page": 2}
        self.mock_client.get.assert_called_once_with("dockets/", params=expected_params)
    
    def test_get_court_dockets_default_page(self):
        """Test get_court_dockets with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_court_dockets("scotus")
        
        assert result == mock_response
        expected_params = {"court": "scotus", "page": 1}
        self.mock_client.get.assert_called_once_with("dockets/", params=expected_params)
    
    def test_get_territorial_courts(self):
        """Test get_territorial_courts method."""
        mock_response = {"results": [{"id": "guam", "name": "Guam District Court"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_territorial_courts(page=2)
        
        assert len(result) == 1
        expected_params = {"page": 2, "jurisdiction": "T"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_territorial_courts_default_page(self):
        """Test get_territorial_courts with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_territorial_courts()
        
        expected_params = {"page": 1, "jurisdiction": "T"}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_active_courts(self):
        """Test get_active_courts method."""
        mock_response = {"results": [{"id": "scotus", "name": "Supreme Court"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_active_courts(page=2)
        
        assert len(result) == 1
        expected_params = {"page": 2, "is_active": True}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_active_courts_default_page(self):
        """Test get_active_courts with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_active_courts()
        
        expected_params = {"page": 1, "is_active": True}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_defunct_courts(self):
        """Test get_defunct_courts method."""
        mock_response = {"results": [{"id": "old_court", "name": "Old Court"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_defunct_courts(page=2)
        
        assert len(result) == 1
        expected_params = {"page": 2, "is_active": False}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_get_defunct_courts_default_page(self):
        """Test get_defunct_courts with default page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_defunct_courts()
        
        expected_params = {"page": 1, "is_active": False}
        self.mock_client.get.assert_called_once_with("courts/", params=expected_params)
    
    def test_error_handling_api_error(self):
        """Test error handling for APIError."""
        self.mock_client.get.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            self.api.list_courts()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_court("scotus")
