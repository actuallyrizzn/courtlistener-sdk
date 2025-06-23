"""
Docket Entries API module for CourtListener SDK.

This module provides access to docket entries, which represent individual
filings or events within a docket.
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from ..models.docket_entry import DocketEntry
from ..utils.filters import build_filters

if TYPE_CHECKING:
    from ..client import CourtListenerClient


class DocketEntriesAPI:
    """API client for docket entries endpoints."""
    
    def __init__(self, client: 'CourtListenerClient'):
        """Initialize the Docket Entries API client.
        
        Args:
            client: The main CourtListener client instance
        """
        self.client = client
        self.base_url = "/api/rest/v4/docket-entries/"
    
    def list_entries(self, docket_id: Optional[int] = None, 
                    filters: Optional[Dict[str, Any]] = None,
                    limit: Optional[int] = None) -> List[DocketEntry]:
        """List docket entries with optional filtering.
        
        Args:
            docket_id: Optional docket ID to filter entries by
            filters: Optional dictionary of filters to apply
            limit: Optional limit on number of results
            
        Returns:
            List of DocketEntry objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        params = {}
        
        if docket_id:
            params['docket'] = docket_id
            
        if filters:
            params.update(build_filters(**filters))
            
        if limit:
            params['limit'] = limit
            
        response = self.client.get(self.base_url, params=params)
        return [DocketEntry.from_dict(entry) for entry in response.get('results', [])]
    
    def get_entry(self, entry_id: int) -> DocketEntry:
        """Get a specific docket entry by ID.
        
        Args:
            entry_id: The ID of the docket entry to retrieve
            
        Returns:
            DocketEntry object
            
        Raises:
            NotFoundError: If the entry is not found
            CourtListenerError: If the API request fails
        """
        url = f"{self.base_url}{entry_id}/"
        response = self.client.get(url)
        return DocketEntry.from_dict(response)
    
    def get_entries_by_date_range(self, docket_id: int, 
                                 start_date: str, 
                                 end_date: str,
                                 limit: Optional[int] = None) -> List[DocketEntry]:
        """Get docket entries within a date range.
        
        Args:
            docket_id: The docket ID to search within
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            limit: Optional limit on number of results
            
        Returns:
            List of DocketEntry objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'docket': docket_id,
            'date_filed__gte': start_date,
            'date_filed__lte': end_date
        }
        return self.list_entries(filters=filters, limit=limit)
    
    def get_entries_by_number(self, docket_id: int, 
                             entry_number: int) -> List[DocketEntry]:
        """Get docket entries by entry number.
        
        Args:
            docket_id: The docket ID to search within
            entry_number: The entry number to search for
            
        Returns:
            List of DocketEntry objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'docket': docket_id,
            'entry_number': entry_number
        }
        return self.list_entries(filters=filters)
    
    def get_entries_by_description(self, docket_id: int, 
                                  description: str,
                                  limit: Optional[int] = None) -> List[DocketEntry]:
        """Get docket entries by description text.
        
        Args:
            docket_id: The docket ID to search within
            description: Text to search for in entry descriptions
            limit: Optional limit on number of results
            
        Returns:
            List of DocketEntry objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'docket': docket_id,
            'description__icontains': description
        }
        return self.list_entries(filters=filters, limit=limit)
    
    def get_entries_with_documents(self, docket_id: int,
                                  limit: Optional[int] = None) -> List[DocketEntry]:
        """Get docket entries that have associated documents.
        
        Args:
            docket_id: The docket ID to search within
            limit: Optional limit on number of results
            
        Returns:
            List of DocketEntry objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'docket': docket_id,
            'recap_documents__isnull': False
        }
        return self.list_entries(filters=filters, limit=limit)

    def list_docket_entries(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('docket-entries/', params=params)

    def search_docket_entries(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('docket-entries/', params=params) 