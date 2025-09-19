"""
RECAP Fetch API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class RecapFetchAPI(BaseAPI):
    """API for managing RECAP fetch operations."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "recap-fetch/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List RECAP fetch operations.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of RECAP fetch operations
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, fetch_id: int) -> Dict[str, Any]:
        """
        Get a specific RECAP fetch operation by ID.
        
        Args:
            fetch_id: RECAP fetch operation ID
        
        Returns:
            RECAP fetch operation data
        """
        return self.client.get(f"{self.endpoint}{fetch_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated RECAP fetch operations.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for RECAP fetch operations
        """
        return self.client.paginate(self.endpoint, params=kwargs)
