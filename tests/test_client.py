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