"""
Pytest configuration for CourtListener SDK tests.
"""

import os
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


# Skip live and E2E tests unless CL_RUN_LIVE environment variable is set
skip_live_tests = pytest.mark.skipif(
    os.getenv("CL_RUN_LIVE") != "1",
    reason="Live tests require CL_RUN_LIVE=1 environment variable"
)

skip_e2e_tests = pytest.mark.skipif(
    os.getenv("CL_RUN_LIVE") != "1",
    reason="E2E tests require CL_RUN_LIVE=1 environment variable"
) 