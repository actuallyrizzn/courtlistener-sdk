"""
Async client class for the CourtListener SDK.

This module provides an async interface for interacting with the CourtListener API
using httpx for async HTTP requests.
"""

import logging
from typing import Dict, Any, Optional

from .config import Config
from .exceptions import CourtListenerError
from .async_transport import AsyncTransport
from .async_endpoints import AsyncEndpointRegistry


class AsyncCourtListenerClient:
    """Async client for interacting with the CourtListener API.
    
    This client provides async/await support for all API endpoints using httpx.
    It should be used with Python's async context manager:
    
    Example:
        async with AsyncCourtListenerClient() as client:
            dockets = await client.dockets.list(page=1)
            for docket in dockets['results']:
                print(docket['case_name'])
    
    Note:
        - All API calls must be awaited
        - The client must be used as an async context manager
        - Pagination iterators are async iterators
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        rate_limit_delay: Optional[float] = None,
    ):
        """
        Initialize async CourtListener client.
        
        Args:
            api_token: CourtListener API token
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
            rate_limit_delay: Delay when rate limited in seconds
        """
        self.config = Config(
            api_token=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            rate_limit_delay=rate_limit_delay,
        )
        
        # Initialize transport layer (will be set up in __aenter__)
        self.transport = None
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Registry will be initialized after transport is ready
        self.registry = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.transport = AsyncTransport(self.config)
        await self.transport.__aenter__()
        
        # Initialize API endpoint registry
        self.registry = AsyncEndpointRegistry(self)
        
        # Expose endpoint modules as client attributes
        self._expose_endpoints()
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.transport:
            await self.transport.__aexit__(exc_type, exc_val, exc_tb)
    
    def _expose_endpoints(self):
        """Expose endpoint modules as client attributes."""
        # Core endpoints
        self.courts = self.registry.courts
        self.clusters = self.registry.clusters
        self.opinions = self.registry.opinions
        self.dockets = self.registry.dockets
        self.judges = self.registry.judges
        self.opinion_clusters = self.registry.opinion_clusters
        
        # Additional endpoints
        self.positions = self.registry.positions
        self.financial = self.registry.financial
        self.audio = self.registry.audio
        self.search = self.registry.search
        
        # Extended endpoints
        self.docket_entries = self.registry.docket_entries
        self.attorneys = self.registry.attorneys
        self.parties = self.registry.parties
        self.documents = self.registry.documents
        self.citations = self.registry.citations
        self.recap_documents = self.registry.recap_documents
        self.financial_disclosures = self.registry.financial_disclosures
        self.investments = self.registry.investments
        self.non_investment_incomes = self.registry.non_investment_incomes
        self.agreements = self.registry.agreements
        self.gifts = self.registry.gifts
        self.reimbursements = self.registry.reimbursements
        self.debts = self.registry.debts
        self.disclosure_positions = self.registry.disclosure_positions
        self.spouse_incomes = self.registry.spouse_incomes
        self.opinions_cited = self.registry.opinions_cited
        self.alerts = self.registry.alerts
        self.docket_alerts = self.registry.docket_alerts
        self.people = self.registry.people
        self.schools = self.registry.schools
        self.educations = self.registry.educations
        self.sources = self.registry.sources
        self.retention_events = self.registry.retention_events
        self.aba_ratings = self.registry.aba_ratings
        self.political_affiliations = self.registry.political_affiliations
        self.tag = self.registry.tag
        self.recap_fetch = self.registry.recap_fetch
        self.recap_query = self.registry.recap_query
        self.originating_court_information = self.registry.originating_court_information
        self.fjc_integrated_database = self.registry.fjc_integrated_database
    
    @property
    def api_token(self) -> Optional[str]:
        """Get the API token."""
        return self.config.api_token
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async GET request to API endpoint."""
        if not self.transport:
            raise CourtListenerError("Client must be used as an async context manager")
        return await self.transport.get(endpoint, params)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async POST request to API endpoint."""
        if not self.transport:
            raise CourtListenerError("Client must be used as an async context manager")
        return await self.transport.post(endpoint, data, json_data)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async PUT request to API endpoint."""
        if not self.transport:
            raise CourtListenerError("Client must be used as an async context manager")
        return await self.transport.put(endpoint, data, json_data)
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async PATCH request to API endpoint."""
        if not self.transport:
            raise CourtListenerError("Client must be used as an async context manager")
        return await self.transport.patch(endpoint, data, json_data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make async DELETE request to API endpoint."""
        if not self.transport:
            raise CourtListenerError("Client must be used as an async context manager")
        return await self.transport.delete(endpoint)
    
    async def test_connection(self) -> bool:
        """
        Test async API connection by making a simple request.
        
        Returns:
            True if connection is successful
        
        Raises:
            CourtListenerError if connection fails
        """
        try:
            # Try to get courts list as a simple test
            await self.get('courts/')
            return True
        except Exception as e:
            raise CourtListenerError(f"Connection test failed: {str(e)}")
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"AsyncCourtListenerClient(base_url='{self.config.base_url}')"


__all__ = ['AsyncCourtListenerClient']
