"""
Pytest configuration for CourtListener SDK tests.
"""

import pytest
from courtlistener import CourtListenerClient


@pytest.fixture
def client():
    """Create a test client instance."""
    return CourtListenerClient(api_token="test_token")


@pytest.fixture
def mock_api_response():
    """Sample API response for testing."""
    return {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 123,
                "name": "Test Item",
                "created_at": "2023-01-01T00:00:00Z"
            }
        ]
    } 