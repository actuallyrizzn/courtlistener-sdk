"""
RECAP Documents API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class RecapDocumentsAPI(BaseAPI):
    """API for accessing RECAP documents."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "recap-documents/"
    
    def list(
        self,
        docket: Optional[int] = None,
        docket_entry: Optional[int] = None,
        court: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List RECAP documents.
        
        Args:
            docket: Filter by docket ID
            docket_entry: Filter by docket entry ID
            court: Filter by court ID or slug
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of RECAP documents
        """
        params = {}
        if docket is not None:
            params['docket'] = docket
        if docket_entry is not None:
            params['docket_entry'] = docket_entry
        if court is not None:
            params['court'] = court
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, doc_id: int) -> Dict[str, Any]:
        """
        Get a specific RECAP document by ID.
        
        Args:
            doc_id: RECAP document ID
        
        Returns:
            RECAP document data
        """
        return self.client.get(f"{self.endpoint}{doc_id}/")
    
    def paginate(
        self,
        docket: Optional[int] = None,
        docket_entry: Optional[int] = None,
        court: Optional[str] = None,
        **kwargs
    ):
        """
        Get paginated RECAP documents.
        
        Args:
            docket: Filter by docket ID
            docket_entry: Filter by docket entry ID
            court: Filter by court ID or slug
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for RECAP documents
        """
        params = {}
        if docket is not None:
            params['docket'] = docket
        if docket_entry is not None:
            params['docket_entry'] = docket_entry
        if court is not None:
            params['court'] = court
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
