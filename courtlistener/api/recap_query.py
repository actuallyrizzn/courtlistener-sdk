"""
RECAP Query API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class RecapQueryAPI(BaseAPI):
    """API for querying RECAP database."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "recap-query/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List RECAP query operations.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of RECAP query operations
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, query_id: int) -> Dict[str, Any]:
        """
        Get a specific RECAP query operation by ID.
        
        Args:
            query_id: RECAP query operation ID
        
        Returns:
            RECAP query operation data
        """
        return self.client.get(f"{self.endpoint}{query_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated RECAP query operations.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for RECAP query operations
        """
        return self.client.paginate(self.endpoint, params=kwargs)
