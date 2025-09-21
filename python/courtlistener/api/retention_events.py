"""
Retention Events API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class RetentionEventsAPI(BaseAPI):
    """API for accessing data retention events."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "retention-events/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List retention events.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of retention events
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, event_id: int) -> Dict[str, Any]:
        """
        Get a specific retention event by ID.
        
        Args:
            event_id: Retention event ID
        
        Returns:
            Retention event data
        """
        return self.client.get(f"{self.endpoint}{event_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated retention events.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for retention events
        """
        return self.client.paginate(self.endpoint, params=kwargs)
