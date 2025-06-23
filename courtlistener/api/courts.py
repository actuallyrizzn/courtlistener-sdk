"""Courts API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..models.base import BaseModel


class Court(BaseModel):
    """Model for court data."""
    pass


class CourtsAPI:
    """API client for courts functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_courts(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List courts with optional filtering, pagination, and search."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('courts/', params=params)
    
    def get_court(self, court_id: str) -> Court:
        """Get a specific court by ID."""
        data = self.client.get(f'courts/{court_id}/')
        return Court(data)

    def get_court_by_url(self, url_slug: str) -> Court:
        """Get a court by its URL slug."""
        data = self.client.get(f'courts/{url_slug}/')
        return Court(data)

    def get_federal_courts(self, page: int = 1) -> Dict[str, Any]:
        """Get all federal courts."""
        params = {'jurisdiction': 'F', 'page': page}
        return self.client.get('courts/', params=params)

    def get_state_courts(self, page: int = 1) -> Dict[str, Any]:
        """Get all state courts."""
        params = {'jurisdiction': 'S', 'page': page}
        return self.client.get('courts/', params=params)

    def get_court_opinions(self, court_id: str, page: int = 1) -> Dict[str, Any]:
        """Get opinions for a specific court."""
        params = {'court': court_id, 'page': page}
        return self.client.get('opinions/', params=params)

    def get_court_dockets(self, court_id: str, page: int = 1) -> Dict[str, Any]:
        """Get dockets for a specific court."""
        params = {'court': court_id, 'page': page}
        return self.client.get('dockets/', params=params) 