"""
Political Affiliations API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class PoliticalAffiliationsAPI(BaseAPI):
    """API for accessing political affiliations data."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "political-affiliations/"
    
    def list(
        self,
        person: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List political affiliations.
        
        Args:
            person: Filter by person ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of political affiliations
        """
        params = {}
        if person is not None:
            params['person'] = person
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, affiliation_id: int) -> Dict[str, Any]:
        """
        Get a specific political affiliation by ID.
        
        Args:
            affiliation_id: Political affiliation ID
        
        Returns:
            Political affiliation data
        """
        return self.client.get(f"{self.endpoint}{affiliation_id}/")
    
    def paginate(
        self,
        person: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated political affiliations.
        
        Args:
            person: Filter by person ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for political affiliations
        """
        params = {}
        if person is not None:
            params['person'] = person
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
