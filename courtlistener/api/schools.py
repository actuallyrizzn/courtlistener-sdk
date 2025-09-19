"""
Schools API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class SchoolsAPI(BaseAPI):
    """API for accessing educational institutions data."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "schools/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List schools.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of schools
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, school_id: int) -> Dict[str, Any]:
        """
        Get a specific school by ID.
        
        Args:
            school_id: School ID
        
        Returns:
            School data
        """
        return self.client.get(f"{self.endpoint}{school_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated schools.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for schools
        """
        return self.client.paginate(self.endpoint, params=kwargs)
