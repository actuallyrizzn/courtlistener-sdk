"""
Dockets API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List, Iterator, Union
from ..utils.filters import build_filters, build_date_range_filter, combine_filters
from ..utils.pagination import PageIterator
from ..utils.validators import validate_id, validate_docket_number
from ..models.base import BaseModel
from ..models.docket import Docket
from .base import BaseAPI


class DocketsAPI(BaseAPI):
    """API client for dockets functionality."""
    
    def __init__(self, client):
        """Initialize Dockets API client."""
        self.client = client
        self.base_url = f"{client.config.base_url}/dockets"
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "dockets/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Docket
    
    def list_dockets(self, page: int = 1, **filters) -> List[Docket]:
        """
        List dockets with optional filtering and pagination.
        """
        params = {"page": page, **filters}
        response = self.client._make_request("GET", self.base_url, params=params)
        dockets = []
        for docket_data in response.get("results", []):
            dockets.append(Docket(docket_data))
        return dockets
    
    def get_docket(self, docket_id: int) -> Docket:
        """
        Get a specific docket by ID.
        
        Args:
            docket_id: Docket ID
        
        Returns:
            Docket object
        
        Raises:
            NotFoundError: If docket not found
        """
        url = f"{self.base_url}/{docket_id}"
        response = self.client._make_request("GET", url)
        return Docket(response)
    
    def get_docket_by_number(
        self,
        docket_number: str,
        court: Optional[str] = None,
    ) -> Optional[Docket]:
        """
        Get docket by docket number.
        
        Args:
            docket_number: Docket number
            court: Court ID to filter by
        
        Returns:
            Docket object or None if not found
        """
        validate_docket_number(docket_number)
        
        filters = {'docket_number': docket_number}
        if court:
            filters['court'] = court
        
        response = self.list_dockets(filters)
        
        if response:
            return response[0]
        return None
    
    def get_dockets_by_court(
        self,
        court_id: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get dockets for a specific court.
        
        Args:
            court_id: Court ID
            filters: Additional filters
        
        Returns:
            Paginated docket results
        """
        court_filters = {'court': court_id}
        if filters:
            court_filters.update(filters)
        
        return self.list_dockets(court_filters)
    
    def get_dockets_by_date_range(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        court: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Get dockets within a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            court: Court ID to filter by
            filters: Additional filters
        
        Returns:
            Paginated docket results
        """
        date_filters = build_date_range_filter('date_filed', start_date, end_date)
        
        all_filters = [date_filters]
        if court:
            all_filters.append({'court': court})
        if filters:
            all_filters.append(filters)
        
        combined_filters = combine_filters(*all_filters)
        return self.list_dockets(combined_filters)
    
    def list_all_dockets(
        self,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Docket]:
        """
        List all dockets and iterate through results.
        
        Args:
            filters: Filter parameters
        
        Yields:
            Docket objects
        """
        paginator = PageIterator(self.client, self.base_url, filters)
        
        for docket_data in paginator:
            yield Docket(docket_data)
    
    def get_dockets_by_court_all(
        self,
        court_id: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Docket]:
        """
        Get all dockets for a court and iterate through results.
        
        Args:
            court_id: Court ID
            filters: Additional filters
        
        Yields:
            Docket objects
        """
        court_filters = {'court': court_id}
        if filters:
            court_filters.update(filters)
        
        return self.list_all_dockets(court_filters)
    
    def search_dockets(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search dockets using the search API.
        
        Args:
            query: Search query
            filters: Additional filters
        
        Returns:
            Search results
        """
        return self.client.search.search_dockets(query, filters)
    
    def search_dockets_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[Docket]:
        """
        Search all dockets and iterate through results.
        
        Args:
            query: Search query
            filters: Additional filters
        
        Yields:
            Docket objects
        """
        search_results = self.client.search.search_dockets_all(query, filters)
        
        for result in search_results:
            # Extract docket data from search result
            if hasattr(result, 'resource_uri') and 'dockets' in result.resource_uri:
                docket_id = result.resource_uri.split('/')[-2]
                yield self.get_docket(int(docket_id)) 