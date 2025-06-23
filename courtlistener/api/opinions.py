"""
Opinions API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, Iterator
from ..utils.filters import build_filters, build_date_range_filter
from ..utils.pagination import PageIterator
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Opinion(BaseModel):
    """Model for opinion data."""
    
    def _parse_data(self):
        """Parse opinion data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed)


class OpinionsAPI:
    """API client for opinions functionality."""
    
    def __init__(self, client):
        """Initialize Opinions API client."""
        self.client = client
    
    def list_opinions(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List opinions with optional filtering."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('opinions/', params=params)
    
    def get_opinion(self, opinion_id: int) -> Opinion:
        """Get a specific opinion by ID."""
        validate_id(opinion_id)
        data = self.client.get(f'opinions/{opinion_id}/')
        return Opinion(data)

    def search_opinions(self, q: str = None, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        if q:
            params['q'] = q
        params['page'] = page
        return self.client.get('opinions/', params=params) 