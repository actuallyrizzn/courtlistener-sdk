"""
Dockets API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List, Iterator, Union
from ..utils.filters import build_filters, build_date_range_filter, combine_filters
from ..utils.pagination import PageIterator
from ..utils.validators import validate_id, validate_docket_number
from ..models.base import BaseModel


class Docket(BaseModel):
    """Model for docket data."""
    
    def _parse_data(self):
        """Parse docket data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed)
        
        # Parse related models if they exist
        if hasattr(self, 'court') and isinstance(self.court, dict):
            from ..models.court import Court
            self.court = self._parse_related_model(self.court, Court)


class DocketsAPI:
    """API client for dockets functionality."""
    
    def __init__(self, client):
        """Initialize Dockets API client."""
        self.client = client
    
    def list_dockets(
        self,
        page: int = 1,
        **filters
    ) -> Dict[str, Any]:
        """
        List dockets with optional filtering and pagination.
        """
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('dockets/', params=params)
    
    def get_docket(self, docket_id: Union[int, str]) -> Docket:
        """
        Get a specific docket by ID.
        
        Args:
            docket_id: Docket ID
        
        Returns:
            Docket object
        
        Raises:
            NotFoundError: If docket not found
        """
        validate_id(docket_id)
        data = self.client.get(f'dockets/{docket_id}/')
        return Docket(data)
    
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
        
        if response.get('results'):
            return Docket(response['results'][0])
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
        paginator = PageIterator(self.client, 'dockets/', filters)
        
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
                yield self.get_docket(docket_id) 