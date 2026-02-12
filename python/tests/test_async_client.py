"""
Tests for the async CourtListener client.
"""

import pytest
import asyncio
from courtlistener import AsyncCourtListenerClient
from courtlistener.exceptions import CourtListenerError


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """Test that the async client works as a context manager."""
    async with AsyncCourtListenerClient(api_token="test_token") as client:
        assert client is not None
        assert client.config.api_token == "test_token"
        assert client.transport is not None


@pytest.mark.asyncio
async def test_async_client_endpoints_initialized():
    """Test that all endpoints are initialized."""
    async with AsyncCourtListenerClient(api_token="test_token") as client:
        # Core endpoints
        assert client.courts is not None
        assert client.dockets is not None
        assert client.opinions is not None
        assert client.clusters is not None
        assert client.judges is not None
        
        # Additional endpoints
        assert client.positions is not None
        assert client.financial is not None
        assert client.audio is not None
        assert client.search is not None
        
        # Extended endpoints
        assert client.docket_entries is not None
        assert client.attorneys is not None
        assert client.parties is not None
        assert client.documents is not None
        assert client.citations is not None
        assert client.recap_documents is not None
        assert client.financial_disclosures is not None
        assert client.investments is not None
        assert client.non_investment_incomes is not None
        assert client.agreements is not None
        assert client.gifts is not None
        assert client.reimbursements is not None
        assert client.debts is not None
        assert client.disclosure_positions is not None
        assert client.spouse_incomes is not None
        assert client.opinions_cited is not None
        assert client.alerts is not None
        assert client.docket_alerts is not None
        assert client.people is not None
        assert client.schools is not None
        assert client.educations is not None
        assert client.sources is not None
        assert client.retention_events is not None
        assert client.aba_ratings is not None
        assert client.political_affiliations is not None
        assert client.tag is not None
        assert client.recap_fetch is not None
        assert client.recap_query is not None
        assert client.originating_court_information is not None
        assert client.fjc_integrated_database is not None


@pytest.mark.asyncio
async def test_async_client_without_context_manager():
    """Test that methods fail without context manager."""
    client = AsyncCourtListenerClient(api_token="test_token")
    
    with pytest.raises(CourtListenerError, match="must be used as an async context manager"):
        await client.get("courts/")


@pytest.mark.asyncio
async def test_async_client_config():
    """Test client configuration."""
    async with AsyncCourtListenerClient(
        api_token="test_token",
        timeout=60,
        max_retries=5,
        retry_delay=2.0,
        rate_limit_delay=3.0
    ) as client:
        assert client.config.api_token == "test_token"
        assert client.config.timeout == 60
        assert client.config.max_retries == 5
        assert client.config.retry_delay == 2.0
        assert client.config.rate_limit_delay == 3.0


@pytest.mark.asyncio
async def test_async_client_repr():
    """Test string representation of async client."""
    async with AsyncCourtListenerClient(api_token="test_token") as client:
        repr_str = repr(client)
        assert "AsyncCourtListenerClient" in repr_str
        assert "base_url" in repr_str


def test_async_client_basic_usage():
    """Test basic async client usage pattern."""
    async def example_usage():
        async with AsyncCourtListenerClient(api_token="test_token") as client:
            # This would make real requests in integration tests
            assert client.dockets is not None
            return True
    
    result = asyncio.run(example_usage())
    assert result is True


@pytest.mark.asyncio
async def test_async_endpoint_methods():
    """Test that async endpoints have the expected methods."""
    async with AsyncCourtListenerClient(api_token="test_token") as client:
        # Check that endpoints have async methods
        assert hasattr(client.dockets, 'list')
        assert hasattr(client.dockets, 'get')
        assert hasattr(client.dockets, 'create')
        assert hasattr(client.dockets, 'update')
        assert hasattr(client.dockets, 'delete')
        
        # Check search endpoint has search method
        assert hasattr(client.search, 'search')
