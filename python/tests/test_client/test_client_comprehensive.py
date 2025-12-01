"""
Comprehensive tests for the CourtListenerClient class.
"""

import pytest
import time
from unittest.mock import Mock, patch, MagicMock
import requests
from courtlistener import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError,
    ConnectionError,
    TimeoutError,
    ValidationError,
)


class TestDisabledEndpoint:
    """Test cases for DisabledEndpoint class."""

    def test_init(self):
        """Test DisabledEndpoint initialization."""
        from courtlistener.client import DisabledEndpoint
        endpoint = DisabledEndpoint("test_endpoint", "not available")
        assert endpoint.endpoint_name == "test_endpoint"
        assert endpoint.reason == "not available"

    def test_getattr_raises_error(self):
        """Test that any method call raises informative error."""
        from courtlistener.client import DisabledEndpoint
        endpoint = DisabledEndpoint("test_endpoint", "not available")
        
        with pytest.raises(CourtListenerError, match="Endpoint 'test_endpoint' is disabled"):
            endpoint.any_method()

    def test_getattr_with_args(self):
        """Test that method calls with args raise error."""
        from courtlistener.client import DisabledEndpoint
        endpoint = DisabledEndpoint("test_endpoint", "not available")
        
        with pytest.raises(CourtListenerError, match="Endpoint 'test_endpoint' is disabled"):
            endpoint.any_method("arg1", "arg2", kwarg="value")


class TestCourtListenerClient:
    """Test cases for CourtListenerClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.api_token = "test_token_123"
        self.client = CourtListenerClient(api_token=self.api_token)

    def test_init_basic(self):
        """Test basic client initialization."""
        client = CourtListenerClient(api_token="test_token")
        assert client.api_token == "test_token"
        assert client.config.api_token == "test_token"
        assert hasattr(client, 'session')
        assert hasattr(client, 'logger')

    def test_init_with_all_params(self):
        """Test client initialization with all parameters."""
        client = CourtListenerClient(
            api_token="test_token",
            base_url="https://custom.api.com",
            timeout=60,
            max_retries=5,
            retry_delay=2.0,
            rate_limit_delay=1.0
        )
        assert client.api_token == "test_token"
        assert client.config.base_url == "https://custom.api.com"
        assert client.config.timeout == 60
        assert client.config.max_retries == 5
        assert client.config.retry_delay == 2.0
        assert client.config.rate_limit_delay == 1.0

    def test_init_with_none_params(self):
        """Test client initialization with None parameters."""
        with pytest.raises(ValidationError, match="API token is required"):
            CourtListenerClient()

    def test_api_token_property(self):
        """Test api_token property."""
        client = CourtListenerClient(api_token="test_token")
        assert client.api_token == "test_token"

    def test_init_api_modules(self):
        """Test that API modules are initialized."""
        client = CourtListenerClient(api_token="test_token")
        
        # Check core modules
        assert hasattr(client, 'courts')
        assert hasattr(client, 'clusters')
        assert hasattr(client, 'opinions')
        assert hasattr(client, 'dockets')
        assert hasattr(client, 'judges')
        assert hasattr(client, 'search')
        
        # Check new modules
        assert hasattr(client, 'docket_entries')
        assert hasattr(client, 'attorneys')
        assert hasattr(client, 'parties')
        assert hasattr(client, 'documents')
        assert hasattr(client, 'citations')
        assert hasattr(client, 'recap_documents')
        assert hasattr(client, 'financial_disclosures')
        assert hasattr(client, 'investments')
        assert hasattr(client, 'non_investment_incomes')
        assert hasattr(client, 'agreements')
        assert hasattr(client, 'gifts')
        assert hasattr(client, 'reimbursements')
        assert hasattr(client, 'debts')
        assert hasattr(client, 'disclosure_positions')
        assert hasattr(client, 'spouse_incomes')
        assert hasattr(client, 'opinions_cited')
        assert hasattr(client, 'alerts')
        assert hasattr(client, 'docket_alerts')
        assert hasattr(client, 'people')
        assert hasattr(client, 'schools')
        assert hasattr(client, 'educations')
        assert hasattr(client, 'sources')
        assert hasattr(client, 'retention_events')
        assert hasattr(client, 'aba_ratings')
        assert hasattr(client, 'political_affiliations')
        assert hasattr(client, 'tag')
        assert hasattr(client, 'recap_fetch')
        assert hasattr(client, 'recap_query')
        assert hasattr(client, 'originating_court_information')
        assert hasattr(client, 'fjc_integrated_database')

    def test_opinion_clusters_alias(self):
        """Test that opinion_clusters is an alias for clusters."""
        client = CourtListenerClient(api_token="test_token")
        assert client.opinion_clusters is client.clusters

    @patch('requests.Session.request')
    def test_make_request_get_success(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "count": 0}
        mock_request.return_value = mock_response

        result = self.client._make_request('GET', 'courts/')
        
        assert result == {"results": [], "count": 0}
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_make_request_post_success(self, mock_request):
        """Test successful POST request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        result = self.client._make_request('POST', 'search/', json_data={"q": "test"})
        
        assert result == {"success": True}
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_make_request_with_params(self, mock_request):
        """Test request with query parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_request.return_value = mock_response

        result = self.client._make_request('GET', 'courts/', params={"page": 1})
        
        assert result == {"results": []}
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_make_request_with_data(self, mock_request):
        """Test request with form data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_request.return_value = mock_response

        result = self.client._make_request('POST', 'search/', data={"q": "test"})
        
        assert result == {"success": True}
        mock_request.assert_called_once()

    @patch('requests.Session.request')
    def test_make_request_url_construction_absolute(self, mock_request):
        """Test URL construction with absolute path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_request.return_value = mock_response

        self.client._make_request('GET', '/courts/')
        
        # Check that URL was constructed correctly
        call_args = mock_request.call_args
        assert '/courts/' in call_args[0][1]  # URL is second positional arg

    @patch('requests.Session.request')
    def test_make_request_url_construction_relative(self, mock_request):
        """Test URL construction with relative path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_request.return_value = mock_response

        self.client._make_request('GET', 'courts/')
        
        # Check that URL was constructed correctly
        call_args = mock_request.call_args
        assert 'courts/' in call_args[0][1]  # URL is second positional arg

    @patch('requests.Session.request')
    def test_make_request_authentication_error(self, mock_request):
        """Test handling of authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError, match="Invalid API token"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_not_found_error(self, mock_request):
        """Test handling of not found error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError, match="Resource not found"):
            self.client._make_request('GET', 'courts/999/')

    @patch('requests.Session.request')
    def test_make_request_rate_limit_error(self, mock_request):
        """Test handling of rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {}
        mock_response.json.return_value = {'detail': 'Rate limit exceeded'}
        mock_request.return_value = mock_response

        # With retry logic, it will retry max_retries times before raising
        # Set max_retries to 0 to test immediate failure
        self.client.config.max_retries = 0
        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_server_error(self, mock_request):
        """Test handling of server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        with pytest.raises(APIError, match="Server error: 500"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_other_error_with_json(self, mock_request):
        """Test handling of other error with JSON response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Bad request"}
        mock_request.return_value = mock_response

        with pytest.raises(APIError, match="Bad request"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_other_error_without_json(self, mock_request):
        """Test handling of other error without JSON response."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_request.return_value = mock_response

        with pytest.raises(APIError, match="HTTP 400"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_timeout_retry(self, mock_request):
        """Test timeout handling with retry."""
        # First call times out, second succeeds
        mock_request.side_effect = [
            requests.exceptions.Timeout("Timeout"),
            Mock(status_code=200, json=lambda: {"results": []})
        ]

        result = self.client._make_request('GET', 'courts/')
        
        assert result == {"results": []}
        assert mock_request.call_count == 2

    @patch('requests.Session.request')
    def test_make_request_connection_error_retry(self, mock_request):
        """Test connection error handling with retry."""
        # First call fails with connection error, second succeeds
        mock_request.side_effect = [
            requests.exceptions.ConnectionError("Connection failed"),
            Mock(status_code=200, json=lambda: {"results": []})
        ]

        result = self.client._make_request('GET', 'courts/')
        
        assert result == {"results": []}
        assert mock_request.call_count == 2

    @patch('requests.Session.request')
    def test_make_request_general_exception_retry(self, mock_request):
        """Test general exception handling with retry."""
        # First call fails with general exception, second succeeds
        mock_request.side_effect = [
            requests.exceptions.RequestException("Request failed"),
            Mock(status_code=200, json=lambda: {"results": []})
        ]

        result = self.client._make_request('GET', 'courts/')
        
        assert result == {"results": []}
        assert mock_request.call_count == 2

    @patch('requests.Session.request')
    def test_make_request_api_error_retry(self, mock_request):
        """Test API error handling with retry."""
        # First call fails with API error, second succeeds
        mock_request.side_effect = [
            APIError("API error"),
            Mock(status_code=200, json=lambda: {"results": []})
        ]

        result = self.client._make_request('GET', 'courts/')
        
        assert result == {"results": []}
        assert mock_request.call_count == 2

    @patch('requests.Session.request')
    def test_make_request_max_retries_exceeded(self, mock_request):
        """Test behavior when max retries are exceeded."""
        mock_request.side_effect = requests.exceptions.Timeout("Timeout")

        with pytest.raises(TimeoutError, match="Request timed out"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_connection_error_max_retries(self, mock_request):
        """Test connection error when max retries exceeded."""
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")

        with pytest.raises(ConnectionError, match="Failed to connect to API"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_general_exception_max_retries(self, mock_request):
        """Test general exception when max retries exceeded."""
        mock_request.side_effect = requests.exceptions.RequestException("Request failed")

        with pytest.raises(CourtListenerError, match="Request failed: Request failed"):
            self.client._make_request('GET', 'courts/')

    @patch('requests.Session.request')
    def test_make_request_api_error_max_retries(self, mock_request):
        """Test API error when max retries exceeded."""
        mock_request.side_effect = APIError("API error")

        with pytest.raises(APIError, match="API error"):
            self.client._make_request('GET', 'courts/')

    def test_get_method(self):
        """Test get method."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"results": []}
            
            result = self.client.get('courts/', params={"page": 1})
            
            assert result == {"results": []}
            mock_make_request.assert_called_once_with('GET', 'courts/', params={"page": 1})

    def test_post_method(self):
        """Test post method."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"success": True}
            
            result = self.client.post('search/', data={"q": "test"})
            
            assert result == {"success": True}
            mock_make_request.assert_called_once_with('POST', 'search/', data={"q": "test"}, json_data=None)

    def test_post_method_with_json(self):
        """Test post method with JSON data."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"success": True}
            
            result = self.client.post('search/', json_data={"q": "test"})
            
            assert result == {"success": True}
            mock_make_request.assert_called_once_with('POST', 'search/', data=None, json_data={"q": "test"})

    def test_paginate_method(self):
        """Test paginate method."""
        from courtlistener.utils.pagination import PageIterator
        
        result = self.client.paginate('courts/', params={"page": 1})
        
        assert isinstance(result, PageIterator)
        assert result.client is self.client
        assert result.endpoint == 'courts/'
        assert result.params == {"page": 1}

    @patch.object(CourtListenerClient, 'get')
    def test_test_connection_success(self, mock_get):
        """Test successful connection test."""
        mock_get.return_value = {"results": []}
        
        result = self.client.test_connection()
        
        assert result is True
        mock_get.assert_called_once_with('courts/')

    @patch.object(CourtListenerClient, 'get')
    def test_test_connection_failure(self, mock_get):
        """Test failed connection test."""
        mock_get.side_effect = Exception("Connection failed")
        
        with pytest.raises(CourtListenerError, match="Connection test failed: Connection failed"):
            self.client.test_connection()

    def test_handle_error_401(self):
        """Test _handle_error with 401 status."""
        mock_response = Mock()
        mock_response.status_code = 401
        
        with pytest.raises(AuthenticationError, match="Invalid API token"):
            self.client._handle_error(mock_response)

    def test_handle_error_403(self):
        """Test _handle_error with 403 status."""
        mock_response = Mock()
        mock_response.status_code = 403
        
        with pytest.raises(AuthenticationError, match="Access forbidden"):
            self.client._handle_error(mock_response)

    def test_handle_error_404(self):
        """Test _handle_error with 404 status."""
        mock_response = Mock()
        mock_response.status_code = 404
        
        with pytest.raises(NotFoundError, match="Resource not found"):
            self.client._handle_error(mock_response)

    def test_handle_error_429(self):
        """Test _handle_error with 429 status."""
        mock_response = Mock()
        mock_response.status_code = 429
        
        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            self.client._handle_error(mock_response)

    def test_handle_error_500(self):
        """Test _handle_error with 500 status."""
        mock_response = Mock()
        mock_response.status_code = 500
        
        with pytest.raises(APIError, match="Server error: 500"):
            self.client._handle_error(mock_response)

    def test_handle_error_other(self):
        """Test _handle_error with other status."""
        mock_response = Mock()
        mock_response.status_code = 400
        
        with pytest.raises(APIError, match="API error: 400"):
            self.client._handle_error(mock_response)

    def test_repr(self):
        """Test __repr__ method."""
        client = CourtListenerClient(api_token="test_token")
        repr_str = repr(client)
        assert "CourtListenerClient" in repr_str
        assert "base_url" in repr_str

    def test_request_method(self):
        """Test _request method."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"results": []}
            
            result = self.client._request('GET', 'courts/', params={"page": 1})
            
            assert result == {"results": []}
            mock_make_request.assert_called_once_with('GET', 'courts/', params={"page": 1})

    def test_request_method_with_kwargs(self):
        """Test _request method with various kwargs."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"success": True}
            
            result = self.client._request('POST', 'search/', data={"q": "test"}, json_data={"query": "test"})
            
            assert result == {"success": True}
            mock_make_request.assert_called_once_with('POST', 'search/', data={"q": "test"}, json_data={"query": "test"})

    @patch('time.sleep')
    def test_rate_limit_delay(self, mock_sleep):
        """Test that rate limit delay is applied."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.headers = {'Retry-After': '5'}
            mock_response.json.return_value = {'detail': 'Rate limit exceeded'}
            mock_request.return_value = mock_response

            # Set max_retries to 1 to allow one retry attempt
            self.client.config.max_retries = 1
            with pytest.raises(RateLimitError):
                self.client._make_request('GET', 'courts/')
            
            # With retry logic, sleep is called in _make_request when catching RateLimitError
            # Check that sleep was called (might be called with retry_after or rate_limit_delay)
            assert mock_sleep.called

    @patch('time.sleep')
    def test_retry_delay(self, mock_sleep):
        """Test that retry delay is applied."""
        with patch('requests.Session.request') as mock_request:
            # First call times out, second succeeds
            mock_request.side_effect = [
                requests.exceptions.Timeout("Timeout"),
                Mock(status_code=200, json=lambda: {"results": []})
            ]

            self.client._make_request('GET', 'courts/')
            
            # Check that sleep was called with retry_delay
            mock_sleep.assert_called_with(self.client.config.retry_delay)
