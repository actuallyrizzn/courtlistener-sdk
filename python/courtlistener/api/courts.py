"""
Courts API client for CourtListener.
"""

from typing import List, Optional, Dict, Any, Union
from ..models.court import Court
from ..exceptions import NotFoundError, APIError
from .base import BaseAPI


class CourtsAPI(BaseAPI):
    """API client for courts endpoints."""
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "courts/"
    
    def list(self, page: int = 1, q: str = None, filters: dict = None, **kwargs) -> List[Court]:
        """
        List courts with optional filtering and pagination.
        
        Standard method name for listing resources. This is the preferred method.
        
        Args:
            page: Page number (default: 1)
            q: Search query (optional)
            filters: Filter dictionary (optional)
            **kwargs: Additional filter parameters
        
        Returns:
            List of Court objects
        """
        return self.list_courts(page=page, q=q, filters=filters, **kwargs)
    
    def get(self, court_id: Union[str, int]) -> Court:
        """
        Get a specific court by ID.
        
        Standard method name for getting a resource. This is the preferred method.
        
        Args:
            court_id: Court ID
        
        Returns:
            Court object
        
        Raises:
            NotFoundError: If court not found
        """
        return self.get_court(str(court_id))
    
    def search(self, q: str, page: int = 1, **filters) -> List[Court]:
        """
        Search courts.
        
        Standard method name for searching resources. This is the preferred method.
        
        Args:
            q: Search query
            page: Page number (default: 1)
            **filters: Additional filter parameters
        
        Returns:
            List of Court objects
        """
        return self.search_courts(q=q, page=page, **filters)
    
    def list_courts(self, page: int = 1, q: str = None, filters: dict = None, **kwargs) -> List[Court]:
        """List courts."""
        params = {"page": page}
        if q:
            params["q"] = q
        if filters:
            params.update(filters)
        params.update(kwargs)
        
        response = self.client.get("courts/", params=params)
        return [Court(item) for item in response.get("results", [])]
    
    def get_court(self, court_id: str) -> Court:
        """
        Get a specific court by ID.
        
        Args:
            court_id: Court ID
            
        Returns:
            Court object
            
        Raises:
            NotFoundError: If court not found
        """
        response = self.client.get(f"courts/{court_id}/")
        return Court(response)
    
    def search_courts(self, q: str, page: int = 1, **filters) -> List[Court]:
        """Search courts."""
        return self.list_courts(page=page, q=q, **filters)
    
    def get_federal_courts(self, page: int = 1) -> List[Court]:
        """
        Get federal courts.
        
        Args:
            page: Page number for pagination
            
        Returns:
            List of Court objects
        """
        return self.list_courts(page=page, jurisdiction="F")
    
    def get_state_courts(self, page: int = 1) -> List[Court]:
        """
        Get state courts.
        
        Args:
            page: Page number for pagination
            
        Returns:
            List of Court objects
        """
        return self.list_courts(page=page, jurisdiction="S")
    
    def get_court_by_url(self, court_url: str) -> Court:
        """
        Get court by URL.
        
        Args:
            court_url: Court URL
            
        Returns:
            Court object
        """
        # Extract court ID from URL
        court_id = court_url.rstrip('/').split('/')[-1]
        return self.get_court(court_id)

    def get_court_opinions(self, court_id: str, page: int = 1, **filters) -> Dict[str, Any]:
        """Get opinions for a specific court."""
        params = {'court': court_id, 'page': page}
        params.update(filters)
        return self.client.get('opinions/', params=params)

    def get_court_dockets(self, court_id: str, page: int = 1) -> Dict[str, Any]:
        """Get dockets for a specific court."""
        params = {'court': court_id, 'page': page}
        return self.client.get('dockets/', params=params)
    
    def get_territorial_courts(self, page: int = 1) -> List[Court]:
        """Get territorial courts."""
        return self.list_courts(page=page, jurisdiction="T")
    
    def get_active_courts(self, page: int = 1) -> List[Court]:
        """Get active courts."""
        return self.list_courts(page=page, is_active=True)
    
    def get_defunct_courts(self, page: int = 1) -> List[Court]:
        """Get defunct courts."""
        return self.list_courts(page=page, is_active=False) 