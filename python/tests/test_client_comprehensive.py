"""
Comprehensive tests for CourtListenerClient to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests
from courtlistener.client import CourtListenerClient, DisabledEndpoint
from courtlistener.exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError,
    ConnectionError,
    TimeoutError,
)


class TestDisabledEndpoint:
    """Test DisabledEndpoint class."""
    
    def test_init(self):
        """Test DisabledEndpoint initialization."""
        endpoint = DisabledEndpoint("test_endpoint", "Not available")
        assert endpoint.endpoint_name == "test_endpoint"
        assert endpoint.reason == "Not available"
    
    def test_getattr_raises_error(self):
        """Test that any method call raises informative error."""
        endpoint = DisabledEndpoint("test_endpoint", "Not available")
        
        with pytest.raises(CourtListenerError) as exc_info:
            endpoint.some_method()
        
        assert "Endpoint 'test_endpoint' is disabled" in str(exc_info.value)
        assert "Not available" in str(exc_info.value)


class TestCourtListenerClientComprehensive:
    """Comprehensive tests for CourtListenerClient to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('courtlistener.client.Config') as mock_config_class:
            self.mock_config = Mock()
            self.mock_config.get_headers.return_value = {"Authorization": "Token test-token"}
            self.mock_config.base_url = "https://api.courtlistener.com/api/rest/v4/"
            self.mock_config.timeout = 30
            self.mock_config.max_retries = 3
            self.mock_config.retry_delay = 1.0
            self.mock_config.rate_limit_delay = 2.0
            mock_config_class.return_value = self.mock_config
            
            with patch('courtlistener.client.requests.Session') as mock_session_class:
                self.mock_session = Mock()
                mock_session_class.return_value = self.mock_session
                
                with patch.object(CourtListenerClient, '_init_api_modules'):
                    self.client = CourtListenerClient(
                        api_token="test-token",
                        base_url="https://api.courtlistener.com/api/rest/v4/",
                        timeout=30,
                        max_retries=3,
                        retry_delay=1.0,
                        rate_limit_delay=2.0
                    )
    
    def test_init_with_all_parameters(self):
        """Test client initialization with all parameters."""
        with patch('courtlistener.client.Config') as mock_config_class:
            mock_config = Mock()
            mock_config.get_headers.return_value = {"Authorization": "Token test-token"}
            mock_config_class.return_value = mock_config
            
            with patch('courtlistener.client.requests.Session') as mock_session_class:
                mock_session = Mock()
                mock_session_class.return_value = mock_session
                
                with patch.object(CourtListenerClient, '_init_api_modules'):
                    client = CourtListenerClient(
                        api_token="test-token",
                        base_url="https://api.courtlistener.com/api/rest/v4/",
                        timeout=30,
                        max_retries=3,
                        retry_delay=1.0,
                        rate_limit_delay=2.0
                    )
                    
                    assert client.config == mock_config
                    assert client.session == mock_session
                    mock_config_class.assert_called_once_with(
                        api_token="test-token",
                        base_url="https://api.courtlistener.com/api/rest/v4/",
                        timeout=30,
                        max_retries=3,
                        retry_delay=1.0,
                        rate_limit_delay=2.0
                    )
    
    def test_init_with_minimal_parameters(self):
        """Test client initialization with minimal parameters."""
        with patch('courtlistener.client.Config') as mock_config_class:
            mock_config = Mock()
            mock_config.get_headers.return_value = {}
            mock_config_class.return_value = mock_config
            
            with patch('courtlistener.client.requests.Session') as mock_session_class:
                mock_session = Mock()
                mock_session_class.return_value = mock_session
                
                with patch.object(CourtListenerClient, '_init_api_modules'):
                    client = CourtListenerClient()
                    
                    assert client.config == mock_config
                    assert client.session == mock_session
                    mock_config_class.assert_called_once_with(
                        api_token=None,
                        base_url=None,
                        timeout=None,
                        max_retries=None,
                        retry_delay=None,
                        rate_limit_delay=None
                    )
    
    def test_api_token_property(self):
        """Test api_token property."""
        self.mock_config.api_token = "test-token"
        assert self.client.api_token == "test-token"
    
    def test_make_request_get_success(self):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        self.mock_session.request.return_value = mock_response
        
        result = self.client._make_request('GET', 'courts/', params={"page": 1})
        
        assert result == {"results": []}
        self.mock_session.request.assert_called_once()
        call_args = self.mock_session.request.call_args
        assert call_args[0] == ('GET', 'https://api.courtlistener.com/api/rest/v4/courts/')
        assert call_args[1]['params'] == {"page": 1}
        assert call_args[1]['timeout'] == 30
    
    def test_make_request_post_with_data(self):
        """Test POST request with form data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        self.mock_session.request.return_value = mock_response
        
        result = self.client._make_request('POST', 'alerts/', data={"query": "test"})
        
        assert result == {"id": 1}
        call_args = self.mock_session.request.call_args
        assert call_args[0] == ('POST', 'https://api.courtlistener.com/api/rest/v4/alerts/')
        assert call_args[1]['data'] == {"query": "test"}
    
    def test_make_request_post_with_json(self):
        """Test POST request with JSON data."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1}
        self.mock_session.request.return_value = mock_response
        
        result = self.client._make_request('POST', 'alerts/', json_data={"query": "test"})
        
        assert result == {"id": 1}
        call_args = self.mock_session.request.call_args
        assert call_args[0] == ('POST', 'https://api.courtlistener.com/api/rest/v4/alerts/')
        assert call_args[1]['json'] == {"query": "test"}
    
    def test_make_request_endpoint_starts_with_slash(self):
        """Test request with endpoint starting with slash."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        self.mock_session.request.return_value = mock_response
        
        result = self.client._make_request('GET', '/courts/')
        
        assert result == {"results": []}
        call_args = self.mock_session.request.call_args
        assert call_args[0] == ('GET', 'https://api.courtlistener.com/api/rest/v4/courts/')
    
    def test_make_request_timeout_retry(self):
        """Test request timeout with retry logic."""
        self.mock_session.request.side_effect = [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),  # Final attempt
        ]
        
        with patch('time.sleep') as mock_sleep:
            with pytest.raises(TimeoutError) as exc_info:
                self.client._make_request('GET', 'courts/')
            
            assert "Request timed out" in str(exc_info.value)
            assert mock_sleep.call_count == 3  # 3 retries
    
    def test_make_request_connection_error_retry(self):
        """Test request connection error with retry logic."""
        self.mock_session.request.side_effect = [
            requests.exceptions.ConnectionError(),
            requests.exceptions.ConnectionError(),
            requests.exceptions.ConnectionError(),
            requests.exceptions.ConnectionError(),  # Final attempt
        ]
        
        with patch('time.sleep') as mock_sleep:
            with pytest.raises(ConnectionError) as exc_info:
                self.client._make_request('GET', 'courts/')
            
            assert "Failed to connect to API" in str(exc_info.value)
            assert mock_sleep.call_count == 3  # 3 retries
    
    def test_make_request_generic_request_exception_retry(self):
        """Test request generic RequestException with retry logic."""
        self.mock_session.request.side_effect = [
            requests.exceptions.RequestException("Network error"),
            requests.exceptions.RequestException("Network error"),
            requests.exceptions.RequestException("Network error"),
            requests.exceptions.RequestException("Network error"),  # Final attempt
        ]
        
        with patch('time.sleep') as mock_sleep:
            with pytest.raises(CourtListenerError) as exc_info:
                self.client._make_request('GET', 'courts/')
            
            assert "Request failed: Network error" in str(exc_info.value)
            assert mock_sleep.call_count == 3  # 3 retries
    
    def test_make_request_api_error_retry(self):
        """Test request APIError with retry logic."""
        api_error = APIError("Temporary error")
        self.mock_session.request.side_effect = [
            api_error,
            api_error,
            api_error,
            api_error,  # Final attempt
        ]
        
        with patch('time.sleep') as mock_sleep:
            with pytest.raises(APIError) as exc_info:
                self.client._make_request('GET', 'courts/')
            
            assert "Temporary error" in str(exc_info.value)
            assert mock_sleep.call_count == 3  # 3 retries
    
    def test_make_request_success_after_retry(self):
        """Test request success after retry."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        
        self.mock_session.request.side_effect = [
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            mock_response,  # Success on third attempt
        ]
        
        with patch('time.sleep') as mock_sleep:
            result = self.client._make_request('GET', 'courts/')
            
            assert result == {"results": []}
            assert mock_sleep.call_count == 2  # 2 retries
    
    def test_handle_response_success(self):
        """Test handling successful response."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        
        result = self.client._handle_response(mock_response)
        
        assert result == {"results": []}
    
    def test_handle_response_401_authentication_error(self):
        """Test handling 401 authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        
        with pytest.raises(AuthenticationError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "Invalid API token" in str(exc_info.value)
    
    def test_handle_response_404_not_found_error(self):
        """Test handling 404 not found error."""
        mock_response = Mock()
        mock_response.status_code = 404
        
        with pytest.raises(NotFoundError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "Resource not found" in str(exc_info.value)
    
    def test_handle_response_429_rate_limit_error(self):
        """Test handling 429 rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {}
        
        with pytest.raises(RateLimitError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "Rate limit exceeded" in str(exc_info.value)
        # Note: sleep is no longer called here - retry happens in _make_request loop
    
    def test_handle_response_500_server_error(self):
        """Test handling 500 server error."""
        mock_response = Mock()
        mock_response.status_code = 500
        
        with pytest.raises(APIError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "Server error: 500" in str(exc_info.value)
    
    def test_handle_response_400_with_json_error(self):
        """Test handling 400 error with JSON error message."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Bad request"}
        
        with pytest.raises(APIError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "Bad request" in str(exc_info.value)
    
    def test_handle_response_400_without_json_error(self):
        """Test handling 400 error without JSON error message."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.side_effect = ValueError("Invalid JSON")
        
        with pytest.raises(APIError) as exc_info:
            self.client._handle_response(mock_response)
        
        assert "HTTP 400" in str(exc_info.value)
    
    def test_get_method(self):
        """Test get method."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"results": []}
            
            result = self.client.get('courts/', params={"page": 1})
            
            assert result == {"results": []}
            mock_make_request.assert_called_once_with('GET', 'courts/', params={"page": 1})
    
    def test_post_method_with_data(self):
        """Test post method with data."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"id": 1}
            
            result = self.client.post('alerts/', data={"query": "test"})
            
            assert result == {"id": 1}
            mock_make_request.assert_called_once_with('POST', 'alerts/', data={"query": "test"}, json_data=None)
    
    def test_post_method_with_json_data(self):
        """Test post method with json_data."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"id": 1}
            
            result = self.client.post('alerts/', json_data={"query": "test"})
            
            assert result == {"id": 1}
            mock_make_request.assert_called_once_with('POST', 'alerts/', data=None, json_data={"query": "test"})
    
    def test_paginate_method(self):
        """Test paginate method."""
        with patch('courtlistener.client.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator_class.return_value = mock_paginator
            
            result = self.client.paginate('courts/', params={"page": 1})
            
            assert result == mock_paginator
            mock_paginator_class.assert_called_once_with(self.client, 'courts/', {"page": 1})
    
    def test_test_connection_success(self):
        """Test successful connection test."""
        with patch.object(self.client, 'get') as mock_get:
            mock_get.return_value = {"results": []}
            
            result = self.client.test_connection()
            
            assert result is True
            mock_get.assert_called_once_with('courts/')
    
    def test_test_connection_failure(self):
        """Test failed connection test."""
        with patch.object(self.client, 'get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            with pytest.raises(CourtListenerError) as exc_info:
                self.client.test_connection()
            
            assert "Connection test failed: Connection failed" in str(exc_info.value)
    
    def test_handle_error_401(self):
        """Test _handle_error with 401 status."""
        mock_response = Mock()
        mock_response.status_code = 401
        
        with pytest.raises(AuthenticationError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "Invalid API token" in str(exc_info.value)
    
    def test_handle_error_403(self):
        """Test _handle_error with 403 status."""
        mock_response = Mock()
        mock_response.status_code = 403
        
        with pytest.raises(AuthenticationError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "Access forbidden" in str(exc_info.value)
    
    def test_handle_error_404(self):
        """Test _handle_error with 404 status."""
        mock_response = Mock()
        mock_response.status_code = 404
        
        with pytest.raises(NotFoundError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "Resource not found" in str(exc_info.value)
    
    def test_handle_error_429(self):
        """Test _handle_error with 429 status."""
        mock_response = Mock()
        mock_response.status_code = 429
        
        with pytest.raises(RateLimitError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "Rate limit exceeded" in str(exc_info.value)
    
    def test_handle_error_500(self):
        """Test _handle_error with 500 status."""
        mock_response = Mock()
        mock_response.status_code = 500
        
        with pytest.raises(APIError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "Server error: 500" in str(exc_info.value)
    
    def test_handle_error_other_status(self):
        """Test _handle_error with other status code."""
        mock_response = Mock()
        mock_response.status_code = 418
        
        with pytest.raises(APIError) as exc_info:
            self.client._handle_error(mock_response)
        
        assert "API error: 418" in str(exc_info.value)
    
    def test_repr(self):
        """Test string representation."""
        repr_str = repr(self.client)
        assert "CourtListenerClient" in repr_str
        assert "base_url='https://api.courtlistener.com/api/rest/v4/'" in repr_str
    
    def test_request_method(self):
        """Test _request method for test compatibility."""
        with patch.object(self.client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"results": []}
            
            result = self.client._request('GET', 'courts/', params={"page": 1})
            
            assert result == {"results": []}
            mock_make_request.assert_called_once_with('GET', 'courts/', params={"page": 1})
    
    def test_init_api_modules(self):
        """Test _init_api_modules method."""
        with patch('courtlistener.client.Config') as mock_config_class:
            mock_config = Mock()
            mock_config.get_headers.return_value = {}
            mock_config_class.return_value = mock_config
            
            with patch('courtlistener.client.requests.Session') as mock_session_class:
                mock_session = Mock()
                mock_session_class.return_value = mock_session
                
                client = CourtListenerClient()
                
                # Check that all API modules are initialized
                assert hasattr(client, 'courts')
                assert hasattr(client, 'clusters')
                assert hasattr(client, 'opinions')
                assert hasattr(client, 'dockets')
                assert hasattr(client, 'judges')
                assert hasattr(client, 'opinion_clusters')
                assert hasattr(client, 'positions')
                assert hasattr(client, 'financial')
                assert hasattr(client, 'audio')
                assert hasattr(client, 'search')
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
