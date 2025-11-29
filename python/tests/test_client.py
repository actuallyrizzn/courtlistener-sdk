"""
Tests for the main CourtListener client.
"""

import pytest
from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError


def test_client_initialization():
    """Test client initialization with API token."""
    client = CourtListenerClient(api_token="test_token")
    assert client.config.api_token == "test_token"
    assert client.config.base_url == "https://www.courtlistener.com/api/rest/v4/"


def test_client_initialization_without_token():
    """Test client initialization without API token raises error."""
    with pytest.raises(ValidationError):
        CourtListenerClient()


def test_client_headers():
    """Test that client sets correct headers."""
    client = CourtListenerClient(api_token="test_token")
    headers = client.config.get_headers()
    assert headers["Authorization"] == "Token test_token"
    assert headers["Content-Type"] == "application/json"


def test_client_instantiation():
    client = CourtListenerClient(api_token="dummy")
    assert client.config.api_token == "dummy"
    # Check all API modules are present
    for attr in [
        'search', 'dockets', 'opinions', 'judges', 'courts',
        'parties', 'attorneys', 'documents', 'audio', 'financial',
        'citations', 'docket_entries', 'clusters', 'positions']:
        assert hasattr(client, attr)


def test_missing_token_raises(monkeypatch):
    # Remove env var if present
    monkeypatch.delenv('COURTLISTENER_API_TOKEN', raising=False)
    from courtlistener.config import Config
    with pytest.raises(ValidationError):
        config = Config()
        config.api_token = None
        CourtListenerClient(config=config)


def test_client_make_request_success():
    """Test successful _make_request call."""
    from unittest.mock import Mock, patch
    import requests
    from courtlistener.exceptions import CourtListenerError, AuthenticationError, APIError, NotFoundError, RateLimitError
    
    client = CourtListenerClient(api_token="test_token")
    
    # Mock the session.request method
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    
    with patch.object(client.session, 'request', return_value=mock_response) as mock_request:
        result = client._make_request('GET', 'test/endpoint', params={'key': 'value'})
        
        assert result == {"result": "success"}
        mock_request.assert_called_once()


def test_client_make_request_with_retry():
    """Test _make_request with retry logic."""
    from unittest.mock import Mock, patch
    import requests
    from courtlistener.exceptions import CourtListenerError
    
    client = CourtListenerClient(api_token="test_token")
    
    # Mock the session.request method to fail first, then succeed
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    
    with patch.object(client.session, 'request', side_effect=[
        requests.exceptions.ConnectionError("Connection failed"),
        mock_response
    ]) as mock_request:
        result = client._make_request('GET', 'test/endpoint')
        
        assert result == {"result": "success"}
        assert mock_request.call_count == 2


def test_client_make_request_timeout():
    """Test _make_request with timeout error."""
    from unittest.mock import Mock, patch
    import requests
    from courtlistener.exceptions import TimeoutError
    
    client = CourtListenerClient(api_token="test_token")
    
    with patch.object(client.session, 'request', side_effect=requests.exceptions.Timeout("Request timed out")):
        with pytest.raises(TimeoutError, match="Request timed out"):
            client._make_request('GET', 'test/endpoint')


def test_client_make_request_connection_error():
    """Test _make_request with connection error."""
    from unittest.mock import Mock, patch
    import requests
    from courtlistener.exceptions import ConnectionError
    
    client = CourtListenerClient(api_token="test_token")
    
    with patch.object(client.session, 'request', side_effect=requests.exceptions.ConnectionError("Connection failed")):
        with pytest.raises(ConnectionError, match="Failed to connect to API"):
            client._make_request('GET', 'test/endpoint')


def test_client_handle_response_success():
    """Test _handle_response with successful response."""
    from unittest.mock import Mock
    from courtlistener.exceptions import AuthenticationError, APIError, NotFoundError, RateLimitError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    
    result = client._handle_response(mock_response)
    assert result == {"result": "success"}


def test_client_handle_response_401():
    """Test _handle_response with 401 error."""
    from unittest.mock import Mock
    from courtlistener.exceptions import AuthenticationError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {"detail": "Invalid token"}
    
    with pytest.raises(AuthenticationError, match="Invalid API token"):
        client._handle_response(mock_response)


def test_client_handle_response_403():
    """Test _handle_response with 403 error."""
    from unittest.mock import Mock
    from courtlistener.exceptions import APIError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"detail": "Permission denied"}
    
    with pytest.raises(APIError, match="Permission denied"):
        client._handle_response(mock_response)


def test_client_handle_response_404():
    """Test _handle_response with 404 error."""
    from unittest.mock import Mock
    from courtlistener.exceptions import NotFoundError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"detail": "Not found"}
    
    with pytest.raises(NotFoundError, match="Resource not found"):
        client._handle_response(mock_response)


def test_client_handle_response_429():
    """Test _handle_response with 429 error."""
    from unittest.mock import Mock
    from courtlistener.exceptions import RateLimitError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.json.return_value = {"detail": "Rate limited"}
    
    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        client._handle_response(mock_response)


def test_client_handle_response_500():
    """Test _handle_response with 500 error."""
    from unittest.mock import Mock
    from courtlistener.exceptions import APIError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"detail": "Internal server error"}
    
    with pytest.raises(APIError, match="Server error"):
        client._handle_response(mock_response)


def test_client_handle_response_invalid_json():
    """Test _handle_response with invalid JSON."""
    from unittest.mock import Mock
    from courtlistener.exceptions import APIError
    
    client = CourtListenerClient(api_token="test_token")
    
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_response.text = "Invalid response"
    
    with pytest.raises(APIError, match="HTTP 400"):
        client._handle_response(mock_response) 