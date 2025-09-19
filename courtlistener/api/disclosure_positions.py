"""
Disclosure Positions API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class DisclosurePositionsAPI(BaseAPI):
    """API for accessing disclosure position data from financial disclosures."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "disclosure-positions/"
    
    def list(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List disclosure position records.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of disclosure positions
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, position_id: int) -> Dict[str, Any]:
        """
        Get a specific disclosure position by ID.
        
        Args:
            position_id: Disclosure position ID
        
        Returns:
            Disclosure position data
        """
        return self.client.get(f"{self.endpoint}{position_id}/")
    
    def paginate(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated disclosure positions.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for disclosure positions
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
