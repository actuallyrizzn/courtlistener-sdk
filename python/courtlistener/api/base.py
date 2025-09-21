"""
Base API class for CourtListener API modules.
"""

from typing import Dict, Any, Optional, Iterator, Union
from ..exceptions import CourtListenerError


class BaseAPI:
    """Base class for all API modules."""
    
    def __init__(self, client):
        """Initialize the API module with a client instance."""
        self.client = client
    
    def list(self, **params) -> Dict[str, Any]:
        """
        List resources with optional filtering.
        
        Args:
            **params: Query parameters for filtering and pagination
            
        Returns:
            Dict containing the API response
        """
        endpoint = self._get_endpoint()
        return self.client.get(endpoint, params=params)
    
    def get(self, resource_id: Union[int, str]) -> Dict[str, Any]:
        """
        Get a specific resource by ID.
        
        Args:
            resource_id: The ID of the resource to retrieve
            
        Returns:
            Dict containing the resource data
        """
        endpoint = f"{self._get_endpoint()}{resource_id}/"
        return self.client.get(endpoint)
    
    def paginate(self, **params) -> Iterator[Dict[str, Any]]:
        """
        Paginate through resources.
        
        Args:
            **params: Query parameters for filtering and pagination
            
        Yields:
            Dict containing each page of results
        """
        endpoint = self._get_endpoint()
        return self.client.paginate(endpoint, params=params)
    
    def _get_endpoint(self) -> str:
        """
        Get the API endpoint for this module.
        
        Returns:
            The endpoint string
        """
        # This should be overridden by subclasses
        raise NotImplementedError("Subclasses must implement _get_endpoint")
    
    def _validate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean parameters.
        
        Args:
            params: Parameters to validate
            
        Returns:
            Cleaned parameters
        """
        # Remove None values
        cleaned = {k: v for k, v in params.items() if v is not None}
        return cleaned
