"""
Non-Investment Incomes API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class NonInvestmentIncomesAPI(BaseAPI):
    """API for accessing non-investment income data from financial disclosures."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "non-investment-incomes/"
    
    def list(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List non-investment income records.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of non-investment incomes
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, income_id: int) -> Dict[str, Any]:
        """
        Get a specific non-investment income by ID.
        
        Args:
            income_id: Non-investment income ID
        
        Returns:
            Non-investment income data
        """
        return self.client.get(f"{self.endpoint}{income_id}/")
    
    def paginate(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated non-investment incomes.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for non-investment incomes
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
