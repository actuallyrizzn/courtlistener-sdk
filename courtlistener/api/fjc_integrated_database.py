"""
FJC Integrated Database API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class FJCIntegratedDatabaseAPI(BaseAPI):
    """API for accessing FJC integrated database."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "fjc-integrated-database/"
    
    def list(self, **kwargs) -> Dict[str, Any]:
        """
        List FJC integrated database records.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            API response with paginated list of FJC integrated database records
        """
        return self.client.get(self.endpoint, params=kwargs)
    
    def get(self, record_id: int) -> Dict[str, Any]:
        """
        Get a specific FJC integrated database record by ID.
        
        Args:
            record_id: FJC integrated database record ID
        
        Returns:
            FJC integrated database record data
        """
        return self.client.get(f"{self.endpoint}{record_id}/")
    
    def paginate(self, **kwargs):
        """
        Get paginated FJC integrated database records.
        
        Args:
            **kwargs: Query parameters
        
        Returns:
            PageIterator for FJC integrated database records
        """
        return self.client.paginate(self.endpoint, params=kwargs)
