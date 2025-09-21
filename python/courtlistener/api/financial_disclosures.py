"""
Financial Disclosures API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class FinancialDisclosuresAPI(BaseAPI):
    """API for accessing financial disclosure reports."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "financial-disclosures/"
    
    def list(
        self,
        judge: Optional[int] = None,
        year: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List financial disclosure reports.
        
        Args:
            judge: Filter by judge ID
            year: Filter by disclosure year
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of financial disclosures
        """
        params = {}
        if judge is not None:
            params['judge'] = judge
        if year is not None:
            params['year'] = year
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, disclosure_id: int) -> Dict[str, Any]:
        """
        Get a specific financial disclosure by ID.
        
        Args:
            disclosure_id: Financial disclosure ID
        
        Returns:
            Financial disclosure data
        """
        return self.client.get(f"{self.endpoint}{disclosure_id}/")
    
    def paginate(
        self,
        judge: Optional[int] = None,
        year: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated financial disclosures.
        
        Args:
            judge: Filter by judge ID
            year: Filter by disclosure year
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for financial disclosures
        """
        params = {}
        if judge is not None:
            params['judge'] = judge
        if year is not None:
            params['year'] = year
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
