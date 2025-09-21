"""
Comprehensive tests for Judges API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.judges import JudgesAPI
from courtlistener.models.judge import Judge
from courtlistener.exceptions import NotFoundError, APIError


class TestJudgesAPIComprehensive:
    """Comprehensive tests for JudgesAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client.config.base_url = "https://api.courtlistener.com/api/rest/v4"
        self.api = JudgesAPI(self.mock_client)
    
    def test_init(self):
        """Test JudgesAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "https://api.courtlistener.com/api/rest/v4/people"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "people/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Judge
    
    def test_list_judges_basic(self):
        """Test basic list_judges functionality."""
        mock_response = {
            "results": [
                {"id": 1, "name": "Judge Smith"},
                {"id": 2, "name": "Judge Johnson"}
            ]
        }
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_judges()
        
        assert len(result) == 2
        assert all(isinstance(j, Judge) for j in result)
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params={"page": 1})
    
    def test_list_judges_with_page(self):
        """Test list_judges with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.list_judges(page=2)
        
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params={"page": 2})
    
    def test_list_judges_with_filters(self):
        """Test list_judges with filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"court": "scotus", "is_alive": True}
        self.api.list_judges(page=1, **filters)
        
        expected_params = {"page": 1, "court": "scotus", "is_alive": True}
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params=expected_params)
    
    def test_list_judges_empty_results(self):
        """Test list_judges with empty results."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_judges()
        
        assert result == []
    
    def test_list_judges_no_results_key(self):
        """Test list_judges when response has no results key."""
        mock_response = {}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_judges()
        
        assert result == []
    
    def test_get_judge_success(self):
        """Test get_judge with valid judge ID."""
        mock_response = {"id": 1, "name": "Judge Smith"}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.get_judge(1)
        
        assert isinstance(result, Judge)
        expected_url = f"{self.api.base_url}/1"
        self.mock_client._make_request.assert_called_once_with("GET", expected_url)
    
    def test_get_judge_not_found(self):
        """Test get_judge with non-existent judge ID."""
        self.mock_client._make_request.side_effect = NotFoundError("Judge not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_judge(999)
    
    def test_search_judges_basic(self):
        """Test search_judges without additional filters."""
        mock_response = {
            "results": [
                {"id": 1, "name": "Judge Smith"},
                {"id": 2, "name": "Judge Johnson"}
            ]
        }
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.search_judges("smith")
        
        assert len(result) == 2
        assert all(isinstance(j, Judge) for j in result)
        expected_params = {"q": "smith", "page": 1}
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params=expected_params)
    
    def test_search_judges_with_page(self):
        """Test search_judges with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.search_judges("smith", page=2)
        
        expected_params = {"q": "smith", "page": 2}
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params=expected_params)
    
    def test_search_judges_with_filters(self):
        """Test search_judges with additional filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"court": "scotus", "is_alive": True}
        self.api.search_judges("smith", page=1, **filters)
        
        expected_params = {"q": "smith", "page": 1, "court": "scotus", "is_alive": True}
        self.mock_client._make_request.assert_called_once_with("GET", self.api.base_url, params=expected_params)
    
    def test_search_judges_empty_results(self):
        """Test search_judges with empty results."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.search_judges("nonexistent")
        
        assert result == []
    
    def test_search_judges_no_results_key(self):
        """Test search_judges when response has no results key."""
        mock_response = {}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.search_judges("smith")
        
        assert result == []
    
    def test_error_handling_api_error(self):
        """Test error handling for APIError."""
        self.mock_client._make_request.side_effect = APIError("API Error")
        
        with pytest.raises(APIError):
            self.api.list_judges()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client._make_request.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_judge(1)
