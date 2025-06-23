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
    assert client.config.base_url == "https://www.courtlistener.com/api/rest/v4"


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