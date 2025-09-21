"""
Comprehensive tests for Base API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.base import BaseAPI
from courtlistener.exceptions import CourtListenerError


class ConcreteAPI(BaseAPI):
    """Concrete implementation of BaseAPI for testing."""
    
    def _get_endpoint(self) -> str:
        """Return a test endpoint."""
        return "test/"


class TestBaseAPIComprehensive:
    """Comprehensive tests for BaseAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = ConcreteAPI(self.mock_client)
    
    def test_init(self):
        """Test BaseAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_list_basic(self):
        """Test basic list functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("test/", params={})
    
    def test_list_with_params(self):
        """Test list with parameters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        params = {"page": 2, "q": "test"}
        result = self.api.list(**params)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("test/", params=params)
    
    def test_get_with_int_id(self):
        """Test get with integer ID."""
        mock_response = {"id": 1, "name": "test"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("test/1/")
    
    def test_get_with_str_id(self):
        """Test get with string ID."""
        mock_response = {"id": "test", "name": "test"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get("test")
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("test/test/")
    
    def test_paginate_basic(self):
        """Test basic paginate functionality."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([{"id": 1}, {"id": 2}]))
        self.mock_client.paginate.return_value = mock_paginator
        
        result = list(self.api.paginate())
        
        assert len(result) == 2
        self.mock_client.paginate.assert_called_once_with("test/", params={})
    
    def test_paginate_with_params(self):
        """Test paginate with parameters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        self.mock_client.paginate.return_value = mock_paginator
        
        params = {"page": 2, "q": "test"}
        list(self.api.paginate(**params))
        
        self.mock_client.paginate.assert_called_once_with("test/", params=params)
    
    def test_get_endpoint_not_implemented(self):
        """Test that _get_endpoint raises NotImplementedError when not overridden."""
        base_api = BaseAPI(self.mock_client)
        
        with pytest.raises(NotImplementedError):
            base_api._get_endpoint()
    
    def test_validate_params_removes_none_values(self):
        """Test _validate_params removes None values."""
        params = {"a": 1, "b": None, "c": "test", "d": None}
        result = self.api._validate_params(params)
        
        expected = {"a": 1, "c": "test"}
        assert result == expected
    
    def test_validate_params_keeps_false_values(self):
        """Test _validate_params keeps False values (not None)."""
        params = {"a": 1, "b": False, "c": 0, "d": ""}
        result = self.api._validate_params(params)
        
        assert result == params
    
    def test_validate_params_empty_dict(self):
        """Test _validate_params with empty dict."""
        result = self.api._validate_params({})
        assert result == {}
    
    def test_validate_params_all_none(self):
        """Test _validate_params with all None values."""
        params = {"a": None, "b": None, "c": None}
        result = self.api._validate_params(params)
        
        assert result == {}
    
    def test_list_with_client_error(self):
        """Test list method with client error."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list()
    
    def test_get_with_client_error(self):
        """Test get method with client error."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.get(1)
    
    def test_paginate_with_client_error(self):
        """Test paginate method with client error."""
        self.mock_client.paginate.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            list(self.api.paginate())
    
    def test_validate_params_with_nested_structures(self):
        """Test _validate_params with nested structures."""
        params = {
            "a": 1,
            "b": None,
            "c": {"nested": "value"},
            "d": [1, 2, 3],
            "e": None
        }
        result = self.api._validate_params(params)
        
        expected = {
            "a": 1,
            "c": {"nested": "value"},
            "d": [1, 2, 3]
        }
        assert result == expected
