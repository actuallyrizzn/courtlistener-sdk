"""
Main client class for the CourtListener SDK.

This module provides a high-level facade for interacting with the CourtListener API.
"""

import logging
from typing import Dict, Any, Optional

from ..config import Config
from ..exceptions import CourtListenerError
from ..utils.pagination import PageIterator
from ..transport import Transport
from ..endpoints import EndpointRegistry, DisabledEndpoint


class CourtListenerClient:
    """Main client for interacting with the CourtListener API."""
    
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
        Initialize CourtListener client.
        
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
        
        # Initialize transport layer
        self.transport = Transport(self.config)
        self.session = self.transport.session  # For backward compatibility
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Initialize API endpoint registry
        self.registry = EndpointRegistry(self)
        
        # Expose endpoint modules as client attributes for backward compatibility
        self._expose_endpoints()
    
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
        
        # Disabled endpoints
        self._disabled_endpoints = self.registry._disabled_endpoints
    
    def _init_api_modules(self):
        """Initialize API endpoint modules (backward compatibility)."""
        # This method exists for backward compatibility but is now handled by EndpointRegistry
        pass
    
    @property
    def api_token(self) -> Optional[str]:
        """Get the API token."""
        return self.config.api_token
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to the API (delegates to transport layer).
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON data for POST requests
        
        Returns:
            API response data
        
        Raises:
            Various CourtListenerError subclasses for different error conditions
        """
        return self.transport._make_request(method, endpoint, params, data, json_data)
    
    def _handle_response(self, response):
        """
        Handle API response (delegates to transport layer).
        
        Args:
            response: HTTP response object
        
        Returns:
            Response data as dictionary
        
        Raises:
            Various CourtListenerError subclasses based on response status
        """
        return self.transport._handle_response(response)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to API endpoint."""
        return self.transport.get(endpoint, params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request to API endpoint."""
        return self.transport.post(endpoint, data, json_data)
    
    def paginate(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> PageIterator:
        """
        Get paginated results from an endpoint.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
        
        Returns:
            PageIterator for iterating through results
        """
        return PageIterator(self, endpoint, params)
    
    def test_connection(self) -> bool:
        """
        Test API connection by making a simple request.
        
        Returns:
            True if connection is successful
        
        Raises:
            CourtListenerError if connection fails
        """
        try:
            # Try to get courts list as a simple test
            self.get('courts/')
            return True
        except Exception as e:
            raise CourtListenerError(f"Connection test failed: {str(e)}")
    
    def _handle_error(self, response):
        """
        Handle API errors (backward compatibility wrapper).
        
        This method exists for backward compatibility but delegates to _handle_response.
        """
        from ..exceptions import AuthenticationError, NotFoundError, RateLimitError, APIError
        
        if response.status_code == 401:
            raise AuthenticationError("Invalid API token")
        elif response.status_code == 403:
            raise AuthenticationError("Access forbidden")
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code >= 500:
            raise APIError(f"Server error: {response.status_code}")
        else:
            raise APIError(f"API error: {response.status_code}")
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"CourtListenerClient(base_url='{self.config.base_url}')"

    def _request(self, method: str, endpoint: str, **kwargs):
        """Internal request method for test mocking compatibility."""
        return self._make_request(method, endpoint, **kwargs)


# Re-export DisabledEndpoint for backward compatibility
__all__ = ['CourtListenerClient', 'DisabledEndpoint']
