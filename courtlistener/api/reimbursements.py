"""
Reimbursements API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class ReimbursementsAPI(BaseAPI):
    """API for accessing reimbursements data from financial disclosures."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "reimbursements/"
    
    def list(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List reimbursement records.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of reimbursements
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, reimbursement_id: int) -> Dict[str, Any]:
        """
        Get a specific reimbursement by ID.
        
        Args:
            reimbursement_id: Reimbursement ID
        
        Returns:
            Reimbursement data
        """
        return self.client.get(f"{self.endpoint}{reimbursement_id}/")
    
    def paginate(
        self,
        financial_disclosure: Optional[int] = None,
        judge: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated reimbursements.
        
        Args:
            financial_disclosure: Filter by financial disclosure ID
            judge: Filter by judge ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for reimbursements
        """
        params = {}
        if financial_disclosure is not None:
            params['financial_disclosure'] = financial_disclosure
        if judge is not None:
            params['judge'] = judge
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
