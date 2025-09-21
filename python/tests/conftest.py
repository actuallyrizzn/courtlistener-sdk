"""
Pytest configuration for CourtListener SDK tests.
"""

import pytest
from courtlistener import CourtListenerClient


@pytest.fixture
def client():
    """Create a test client instance."""
    return CourtListenerClient(api_token="7c2ad11c595dcb088f23d7a757190c47e8f397a2")


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