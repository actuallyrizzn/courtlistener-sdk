"""
Main client class for the CourtListener SDK.

This module provides the high-level CourtListenerClient facade that
delegates to the transport layer and endpoint registry.
"""

import logging
from typing import Dict, Any, Optional

from ..config import Config
from ..transport import Transport
from ..endpoints import EndpointRegistry, DisabledEndpoint
from ..utils.pagination import PageIterator
from ..exceptions import CourtListenerError

# Export DisabledEndpoint for backward compatibility
__all__ = ['CourtListenerClient', 'DisabledEndpoint']


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
        # Initialize configuration
        self.config = Config(
            api_token=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            rate_limit_delay=rate_limit_delay,
        )
        
        # Initialize transport layer
        self._transport = Transport(self.config)
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # Initialize endpoint registry
        self._registry = EndpointRegistry(self)
        self._registry.initialize_all()
        
        # Expose endpoints as attributes for backward compatibility
        self._init_endpoint_attributes()
    
    def _init_endpoint_attributes(self):
        """Initialize endpoint attributes for backward compatibility."""
        # Get all endpoints from registry
        endpoints = self._registry.list_endpoints()
        
        # Set each endpoint as an attribute
        for name, endpoint in endpoints.items():
            setattr(self, name, endpoint)
        
        # Legacy disabled endpoints (kept for compatibility)
        self._disabled_endpoints = {}
    
    @property
    def api_token(self) -> Optional[str]:
        """Get the API token."""
        return self.config.api_token
    
    @property
    def session(self):
        """Get the HTTP session (for backward compatibility)."""
        return self._transport.session
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to the API.
        
        This method delegates to the transport layer.
        Kept for backward compatibility with existing code and tests.
        
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
        return self._transport.make_request(method, endpoint, params, data, json_data)
    
    def _handle_response(self, response):
        """
        Handle API response.
        
        Kept for backward compatibility with tests that mock this method.
        Delegates to transport layer's response handler.
        
        Args:
            response: HTTP response object
        
        Returns:
            Response data as dictionary
        """
        return self._transport._handle_response(response)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make GET request to API endpoint.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
        
        Returns:
            API response data
        """
        return self._transport.get(endpoint, params)
    
    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request to API endpoint.
        
        Args:
            endpoint: API endpoint path
            data: Form data
            json_data: JSON data
        
        Returns:
            API response data
        """
        return self._transport.post(endpoint, data, json_data)
    
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
        Handle API errors.
        
        Kept for backward compatibility. Delegates to transport layer.
        
        Args:
            response: HTTP response object
        """
        return self._transport._handle_response(response)
    
    def _request(self, method: str, endpoint: str, **kwargs):
        """
        Internal request method for test mocking compatibility.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters
        
        Returns:
            API response data
        """
        return self._make_request(method, endpoint, **kwargs)
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"CourtListenerClient(base_url='{self.config.base_url}')"
