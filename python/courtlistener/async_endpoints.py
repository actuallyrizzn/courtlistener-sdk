"""
Async API Endpoint Registry for the CourtListener SDK.

This module provides async wrappers for all API endpoints using the same endpoint
structure as the synchronous client, but with async method calls.
"""

from typing import Dict, Any, Optional, List
from .exceptions import CourtListenerError


class AsyncBaseAPI:
    """Base class for async API endpoints."""
    
    def __init__(self, client, endpoint_path: str):
        """
        Initialize async API endpoint.
        
        Args:
            client: AsyncCourtListenerClient instance
            endpoint_path: API endpoint path (e.g., 'dockets/')
        """
        self.client = client
        self.endpoint_path = endpoint_path
    
    async def list(self, page: int = 1, **filters) -> Dict[str, Any]:
        """
        List resources with optional filtering and pagination.
        
        Args:
            page: Page number (default: 1)
            **filters: Additional filter parameters
        
        Returns:
            API response with results list
        """
        params = {'page': page}
        params.update(filters)
        return await self.client.get(self.endpoint_path, params=params)
    
    async def get(self, resource_id: int) -> Dict[str, Any]:
        """
        Get a specific resource by ID.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Resource data
        
        Raises:
            NotFoundError: If resource not found
        """
        endpoint = f"{self.endpoint_path}{resource_id}/"
        return await self.client.get(endpoint)
    
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new resource.
        
        Args:
            data: Resource data
        
        Returns:
            Created resource data
        """
        return await self.client.post(self.endpoint_path, json_data=data)
    
    async def update(self, resource_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing resource.
        
        Args:
            resource_id: Resource ID
            data: Updated resource data
        
        Returns:
            Updated resource data
        """
        endpoint = f"{self.endpoint_path}{resource_id}/"
        return await self.client.put(endpoint, json_data=data)
    
    async def delete(self, resource_id: int) -> Dict[str, Any]:
        """
        Delete a resource.
        
        Args:
            resource_id: Resource ID
        
        Returns:
            Delete response
        """
        endpoint = f"{self.endpoint_path}{resource_id}/"
        return await self.client.delete(endpoint)


class AsyncSearchAPI(AsyncBaseAPI):
    """Async search API wrapper."""
    
    def __init__(self, client):
        super().__init__(client, 'search/')
    
    async def search(self, q: str, type: Optional[str] = None, page: int = 1, **filters) -> Dict[str, Any]:
        """
        Perform a search query.
        
        Args:
            q: Search query
            type: Type of search (optional)
            page: Page number
            **filters: Additional filters
        
        Returns:
            Search results
        """
        params = {'q': q, 'page': page}
        if type:
            params['type'] = type
        params.update(filters)
        return await self.client.get(self.endpoint_path, params=params)


class AsyncEndpointRegistry:
    """Manages async API endpoint modules."""
    
    def __init__(self, client):
        """
        Initialize async endpoint registry.
        
        Args:
            client: AsyncCourtListenerClient instance
        """
        self.client = client
        self._init_api_modules()
    
    def _init_api_modules(self):
        """Initialize async API endpoint modules."""
        # Core endpoints
        self.courts = AsyncBaseAPI(self.client, 'courts/')
        self.clusters = AsyncBaseAPI(self.client, 'clusters/')
        self.opinions = AsyncBaseAPI(self.client, 'opinions/')
        self.dockets = AsyncBaseAPI(self.client, 'dockets/')
        self.judges = AsyncBaseAPI(self.client, 'people/')
        self.opinion_clusters = self.clusters  # Alias for compatibility
        
        # Additional endpoints
        self.positions = AsyncBaseAPI(self.client, 'positions/')
        self.financial = AsyncBaseAPI(self.client, 'financial-disclosures/')
        self.audio = AsyncBaseAPI(self.client, 'audio/')
        self.search = AsyncSearchAPI(self.client)
        
        # Extended endpoints
        self.docket_entries = AsyncBaseAPI(self.client, 'docket-entries/')
        self.attorneys = AsyncBaseAPI(self.client, 'attorneys/')
        self.parties = AsyncBaseAPI(self.client, 'parties/')
        self.documents = AsyncBaseAPI(self.client, 'documents/')
        self.citations = AsyncBaseAPI(self.client, 'citations/')
        self.recap_documents = AsyncBaseAPI(self.client, 'recap-documents/')
        self.financial_disclosures = AsyncBaseAPI(self.client, 'financial-disclosures/')
        self.investments = AsyncBaseAPI(self.client, 'investments/')
        self.non_investment_incomes = AsyncBaseAPI(self.client, 'non-investment-incomes/')
        self.agreements = AsyncBaseAPI(self.client, 'agreements/')
        self.gifts = AsyncBaseAPI(self.client, 'gifts/')
        self.reimbursements = AsyncBaseAPI(self.client, 'reimbursements/')
        self.debts = AsyncBaseAPI(self.client, 'debts/')
        self.disclosure_positions = AsyncBaseAPI(self.client, 'disclosure-positions/')
        self.spouse_incomes = AsyncBaseAPI(self.client, 'spouse-incomes/')
        self.opinions_cited = AsyncBaseAPI(self.client, 'opinions-cited/')
        self.alerts = AsyncBaseAPI(self.client, 'alerts/')
        self.docket_alerts = AsyncBaseAPI(self.client, 'docket-alerts/')
        self.people = AsyncBaseAPI(self.client, 'people/')
        self.schools = AsyncBaseAPI(self.client, 'schools/')
        self.educations = AsyncBaseAPI(self.client, 'educations/')
        self.sources = AsyncBaseAPI(self.client, 'sources/')
        self.retention_events = AsyncBaseAPI(self.client, 'retention-events/')
        self.aba_ratings = AsyncBaseAPI(self.client, 'aba-ratings/')
        self.political_affiliations = AsyncBaseAPI(self.client, 'political-affiliations/')
        self.tag = AsyncBaseAPI(self.client, 'tags/')
        self.recap_fetch = AsyncBaseAPI(self.client, 'recap-fetch/')
        self.recap_query = AsyncBaseAPI(self.client, 'recap-query/')
        self.originating_court_information = AsyncBaseAPI(self.client, 'originating-court-information/')
        self.fjc_integrated_database = AsyncBaseAPI(self.client, 'fjc-integrated-database/')


__all__ = ['AsyncEndpointRegistry', 'AsyncBaseAPI', 'AsyncSearchAPI']
