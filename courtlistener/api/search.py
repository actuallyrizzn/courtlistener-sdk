"""
Search API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List, Iterator
from ..utils.filters import build_filters, combine_filters
from ..utils.pagination import PageIterator
from ..models.base import BaseModel


class SearchResult(BaseModel):
    """Model for search result items."""
    
    def _parse_data(self):
        """Parse search result data."""
        super()._parse_data()
        
        # Add result type detection
        if hasattr(self, 'resource_uri'):
            if 'opinions' in self.resource_uri:
                self.result_type = 'opinion'
            elif 'dockets' in self.resource_uri:
                self.result_type = 'docket'
            elif 'judges' in self.resource_uri:
                self.result_type = 'judge'
            elif 'audio' in self.resource_uri:
                self.result_type = 'audio'
            else:
                self.result_type = 'unknown'


class SearchAPI:
    """API client for search functionality."""
    
    def __init__(self, client):
        """Initialize Search API client."""
        self.client = client
    
    def search(
        self,
        query: str,
        result_type: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Search across all resources.
        
        Args:
            query: Search query string
            result_type: Filter by result type ('o' for opinions, 'd' for dockets, etc.)
            filters: Additional filters to apply
        
        Returns:
            Search results with pagination info
        """
        params = {'q': query}
        
        if result_type:
            params['type'] = result_type
        
        if filters:
            params.update(filters)
        
        return self.client.get('search/', params=params)
    
    def search_opinions(self, q: str = None, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        if q:
            params['q'] = q
        params['page'] = page
        return self.client.get('search/', params=params)
    
    def search_dockets(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search for dockets only."""
        return self.search(query, result_type='d', filters=filters)
    
    def search_judges(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search for judges only."""
        return self.search(query, result_type='j', filters=filters)
    
    def search_audio(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search for audio recordings only."""
        return self.search(query, result_type='oa', filters=filters)
    
    def search_all(
        self,
        query: str,
        result_type: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[SearchResult]:
        """
        Search and iterate through all results.
        
        Args:
            query: Search query string
            result_type: Filter by result type
            filters: Additional filters to apply
        
        Yields:
            SearchResult objects
        """
        params = {'q': query}
        
        if result_type:
            params['type'] = result_type
        
        if filters:
            params.update(filters)
        
        paginator = PageIterator(self.client, 'search/', params)
        
        for result_data in paginator:
            yield SearchResult(result_data)
    
    def search_opinions_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[SearchResult]:
        """Search for all opinions and iterate through results."""
        return self.search_all(query, result_type='o', filters=filters)
    
    def search_dockets_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[SearchResult]:
        """Search for all dockets and iterate through results."""
        return self.search_all(query, result_type='d', filters=filters)
    
    def search_judges_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[SearchResult]:
        """Search for all judges and iterate through results."""
        return self.search_all(query, result_type='j', filters=filters)
    
    def search_audio_all(
        self,
        query: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Iterator[SearchResult]:
        """Search for all audio recordings and iterate through results."""
        return self.search_all(query, result_type='oa', filters=filters) 