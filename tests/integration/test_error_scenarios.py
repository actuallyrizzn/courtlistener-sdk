import os
import pytest
import requests
from unittest.mock import patch, Mock
from courtlistener.client import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError, AuthenticationError, RateLimitError, 
    ValidationError, APIError
)

pytestmark = pytest.mark.integration

API_TOKEN = os.environ.get('COURTLISTENER_API_TOKEN')

@pytest.fixture(scope='module')
def client():
    if not API_TOKEN:
        pytest.skip('No API token set for integration tests')
    return CourtListenerClient(api_token=API_TOKEN)

class TestAuthenticationErrors:
    """Test authentication error scenarios."""
    
    def test_invalid_token(self):
        """Test error handling for invalid authentication token."""
        bad_client = CourtListenerClient(api_token='invalid_token_12345')
        with pytest.raises(AuthenticationError):
            bad_client.search.search_opinions(q='test')
    
    def test_missing_token(self):
        """Test error handling for missing authentication token."""
        bad_client = CourtListenerClient(api_token='')
        with pytest.raises(AuthenticationError):
            bad_client.search.search_opinions(q='test')
    
    def test_expired_token(self):
        """Test error handling for expired token (mocked)."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = AuthenticationError('Token expired')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(AuthenticationError):
                client.search.search_opinions(q='test')

class TestAPIErrors:
    """Test API error scenarios."""
    
    def test_400_bad_request(self, client):
        """Test 400 Bad Request error handling."""
        # Try to create a request with invalid parameters
        with pytest.raises(CourtListenerError) as exc_info:
            client.search.search_opinions(q='', court='invalid_court')
        # Note: This might not always return 400, but should handle errors gracefully
    
    def test_404_not_found(self, client):
        """Test 404 Not Found error handling."""
        with pytest.raises(CourtListenerError) as exc_info:
            client.dockets.get_docket(999999999)
        assert exc_info.value.status_code == 404
    
    def test_404_not_found_opinion(self, client):
        """Test 404 Not Found for opinions."""
        with pytest.raises(CourtListenerError) as exc_info:
            client.opinions.get_opinion(999999999)
        assert exc_info.value.status_code == 404
    
    def test_404_not_found_court(self, client):
        """Test 404 Not Found for courts."""
        with pytest.raises(CourtListenerError) as exc_info:
            client.courts.get_court(999999999)
        assert exc_info.value.status_code == 404
    
    def test_429_rate_limited(self):
        """Test 429 Rate Limited error handling (mocked)."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = RateLimitError('Rate limit exceeded')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(RateLimitError):
                client.search.search_opinions(q='test')
    
    def test_500_server_error(self):
        """Test 500 Server Error handling (mocked)."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = APIError('Internal server error', status_code=500)
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(APIError) as exc_info:
                client.search.search_opinions(q='test')
            assert exc_info.value.status_code == 500

class TestNetworkErrors:
    """Test network error scenarios."""
    
    def test_connection_timeout(self):
        """Test connection timeout error handling."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout('Connection timeout')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(CourtListenerError):
                client.search.search_opinions(q='test')
    
    def test_dns_resolution_failure(self):
        """Test DNS resolution failure error handling."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError('DNS resolution failed')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(CourtListenerError):
                client.search.search_opinions(q='test')
    
    def test_ssl_certificate_issues(self):
        """Test SSL certificate error handling."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.SSLError('SSL certificate error')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(CourtListenerError):
                client.search.search_opinions(q='test')
    
    def test_connection_refused(self):
        """Test connection refused error handling."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError('Connection refused')
            client = CourtListenerClient(api_token='dummy')
            with pytest.raises(CourtListenerError):
                client.search.search_opinions(q='test')

class TestValidationErrors:
    """Test validation error scenarios."""
    
    def test_invalid_date_format(self, client):
        """Test invalid date format error handling."""
        with pytest.raises(ValidationError):
            client.search.search_opinions(
                q='test',
                date_filed_min='invalid-date'
            )
    
    def test_invalid_court_code(self, client):
        """Test invalid court code error handling."""
        with pytest.raises(ValidationError):
            client.search.search_opinions(
                q='test',
                court='invalid_court_code'
            )
    
    def test_invalid_opinion_type(self, client):
        """Test invalid opinion type error handling."""
        with pytest.raises(ValidationError):
            client.opinions.list_opinions(type='invalid_type')

class TestRetryLogic:
    """Test retry logic for transient errors."""
    
    def test_retry_on_timeout(self):
        """Test retry logic on timeout errors."""
        with patch('requests.Session.request') as mock_request:
            # First call fails with timeout, second succeeds
            mock_request.side_effect = [
                requests.exceptions.Timeout('Connection timeout'),
                Mock(status_code=200, json=lambda: {'results': [], 'count': 0})
            ]
            client = CourtListenerClient(api_token='dummy')
            # Should retry and eventually succeed
            resp = client.search.search_opinions(q='test')
            assert 'results' in resp
    
    def test_retry_on_500_error(self):
        """Test retry logic on 500 errors."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            # First call fails with 500, second succeeds
            mock_request.side_effect = [
                APIError('Internal server error', status_code=500),
                {'results': [], 'count': 0}
            ]
            client = CourtListenerClient(api_token='dummy')
            # Should retry and eventually succeed
            resp = client.search.search_opinions(q='test')
            assert 'results' in resp 
