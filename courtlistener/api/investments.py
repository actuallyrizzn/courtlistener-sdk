"""
Investments API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class InvestmentsAPI(BaseAPI):
    """API for accessing investment data from financial disclosures."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "investments/"
    
    def list(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List investment records.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of investments
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, investment_id: int) -> Dict[str, Any]:
        """
        Get a specific investment by ID.
        
        Args:
            investment_id: Investment ID
        
        Returns:
            Investment data
        """
        return self.client.get(f"{self.endpoint}{investment_id}/")
    
    def paginate(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated investments.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for investments
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
