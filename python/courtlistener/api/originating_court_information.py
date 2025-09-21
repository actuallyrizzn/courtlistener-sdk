"""
Originating Court Information API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class OriginatingCourtInformationAPI(BaseAPI):
    """API for accessing originating court information."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "originating-court-information/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List originating court information records.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of originating court information
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, info_id: int) -> Dict[str, Any]:
        """
        Get a specific originating court information by ID.
        
        Args:
            info_id: Originating court information ID
        
        Returns:
            Originating court information data
        """
        return self.client.get(f"{self.endpoint}{info_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated originating court information.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for originating court information
        """
        return self.client.paginate(self.endpoint, params=kwargs)
