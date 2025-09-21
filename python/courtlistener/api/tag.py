"""
Tag API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class TagAPI(BaseAPI):
    """API for accessing tagging system data."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "tag/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List tags.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of tags
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, tag_id: int) -> Dict[str, Any]:
        """
        Get a specific tag by ID.
        
        Args:
            tag_id: Tag ID
        
        Returns:
            Tag data
        """
        return self.client.get(f"{self.endpoint}{tag_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated tags.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for tags
        """
        return self.client.paginate(self.endpoint, params=kwargs)
