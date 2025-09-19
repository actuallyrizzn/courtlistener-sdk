"""
Sources API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class SourcesAPI(BaseAPI):
    """API for accessing data sources information."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "sources/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List data sources.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of sources
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, source_id: int) -> Dict[str, Any]:
        """
        Get a specific source by ID.
        
        Args:
            source_id: Source ID
        
        Returns:
            Source data
        """
        return self.client.get(f"{self.endpoint}{source_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated sources.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for sources
        """
        return self.client.paginate(self.endpoint, params=kwargs)
