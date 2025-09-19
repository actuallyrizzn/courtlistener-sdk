"""
Opinions Cited API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class OpinionsCitedAPI(BaseAPI):
    """API for accessing citation relationships between opinions."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "opinions-cited/"
    
    def list(
        self,
        citing_opinion: Optional[int] = None,
        cited_opinion: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List citation relationships.
        
        Args:
            citing_opinion: Filter by citing opinion ID
            cited_opinion: Filter by cited opinion ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of citation relationships
        """
        params = {}
        if citing_opinion is not None:
            params['citing_opinion'] = citing_opinion
        if cited_opinion is not None:
            params['cited_opinion'] = cited_opinion
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, citation_id: int) -> Dict[str, Any]:
        """
        Get a specific citation relationship by ID.
        
        Args:
            citation_id: Citation relationship ID
        
        Returns:
            Citation relationship data
        """
        return self.client.get(f"{self.endpoint}{citation_id}/")
    
    def paginate(
        self,
        citing_opinion: Optional[int] = None,
        cited_opinion: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated citation relationships.
        
        Args:
            citing_opinion: Filter by citing opinion ID
            cited_opinion: Filter by cited opinion ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for citation relationships
        """
        params = {}
        if citing_opinion is not None:
            params['citing_opinion'] = citing_opinion
        if cited_opinion is not None:
            params['cited_opinion'] = cited_opinion
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
