"""
Pagination utilities for the CourtListener SDK.
"""

from typing import Iterator, Optional, Dict, Any, Callable
from ..exceptions import CourtListenerError


class Paginator:
    """Handles cursor-based pagination for CourtListener API responses."""
    
    def __init__(self, client, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize paginator.
        
        Args:
            client: CourtListener client instance
            endpoint: API endpoint to paginate
            params: Query parameters for the request
        """
        self.client = client
        self.endpoint = endpoint
        self.params = params or {}
        self.cursor = None
        self.has_more = True
    
    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterate through all pages of results."""
        while self.has_more:
            response = self._fetch_page()
            
            if not response or 'results' not in response:
                break
            
            for item in response['results']:
                yield item
            
            # Update pagination state
            next_cursor = response.get('next')
            # Only update cursor if it's different to prevent infinite loops
            if next_cursor != self.cursor:
                self.cursor = next_cursor
                self.has_more = bool(self.cursor)
            else:
                # If cursor hasn't changed, we're stuck in a loop
                self.has_more = False
    
    def _fetch_page(self) -> Optional[Dict[str, Any]]:
        """Fetch a single page of results."""
        params = self.params.copy()
        
        if self.cursor:
            # Extract cursor from next URL
            if 'cursor=' in self.cursor:
                cursor_value = self.cursor.split('cursor=')[1].split('&')[0]
                params['cursor'] = cursor_value
        
        try:
            response = self.client._make_request('GET', self.endpoint, params=params)
            return response
        except Exception as e:
            raise CourtListenerError(f"Failed to fetch page: {str(e)}")


class PageIterator:
    """Iterator for paginated results with lazy loading."""
    
    def __init__(self, client, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """
        Initialize page iterator.
        
        Args:
            client: CourtListener client instance
            endpoint: API endpoint to iterate
            params: Query parameters for the request
        """
        self.client = client
        self.endpoint = endpoint
        self.params = params or {}
        self.current_page = None
        self.current_index = 0
        self.cursor = None
        self.has_more = True
    
    def __iter__(self):
        """Return self as iterator."""
        return self
    
    def __next__(self) -> Dict[str, Any]:
        """Get next item from paginated results."""
        # Load first page if not loaded
        if self.current_page is None:
            self._load_next_page()
        
        # If we've exhausted current page, load next page
        if self.current_index >= len(self.current_page.get('results', [])):
            if not self.has_more:
                raise StopIteration
            self._load_next_page()
        
        # Return current item and advance index
        item = self.current_page['results'][self.current_index]
        self.current_index += 1
        return item
    
    def _load_next_page(self):
        """Load the next page of results."""
        params = self.params.copy()
        
        if self.cursor:
            if 'cursor=' in self.cursor:
                cursor_value = self.cursor.split('cursor=')[1].split('&')[0]
                params['cursor'] = cursor_value
        
        try:
            response = self.client._make_request('GET', self.endpoint, params=params)
            self.current_page = response
            self.current_index = 0
            next_cursor = response.get('next')
            # Only update cursor if it's different to prevent infinite loops
            if next_cursor != self.cursor:
                self.cursor = next_cursor
                self.has_more = bool(self.cursor)
            else:
                # If cursor hasn't changed, we're stuck in a loop
                self.has_more = False
        except Exception as e:
            raise CourtListenerError(f"Failed to load page: {str(e)}")


def paginate_results(client, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
    """
    Convenience function to paginate through API results.
    
    Args:
        client: CourtListener client instance
        endpoint: API endpoint to paginate
        params: Query parameters for the request
    
    Yields:
        Individual result items from all pages
    """
    paginator = Paginator(client, endpoint, params)
    yield from paginator 