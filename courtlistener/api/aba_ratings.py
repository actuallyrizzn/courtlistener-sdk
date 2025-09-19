"""
ABA Ratings API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class ABARatingsAPI(BaseAPI):
    """API for accessing ABA ratings data."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "aba-ratings/"
    
    def list(
        self,
        person: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List ABA ratings.
        
        Args:
            person: Filter by person ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of ABA ratings
        """
        params = {}
        if person is not None:
            params['person'] = person
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, rating_id: int) -> Dict[str, Any]:
        """
        Get a specific ABA rating by ID.
        
        Args:
            rating_id: ABA rating ID
        
        Returns:
            ABA rating data
        """
        return self.client.get(f"{self.endpoint}{rating_id}/")
    
    def paginate(
        self,
        person: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated ABA ratings.
        
        Args:
            person: Filter by person ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for ABA ratings
        """
        params = {}
        if person is not None:
            params['person'] = person
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
