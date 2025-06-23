"""Attorneys API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Attorney(BaseModel):
    """Model for attorney data."""
    pass


class AttorneysAPI:
    """API client for attorneys functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_attorneys(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List attorneys with optional filtering."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('attorneys/', params=params)
    
    def get_attorney(self, attorney_id: int) -> Attorney:
        """Get a specific attorney by ID."""
        validate_id(attorney_id)
        data = self.client.get(f'attorneys/{attorney_id}/')
        return Attorney(data)

    def search_attorneys(self, q: str, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['q'] = q
        params['page'] = page
        return self.client.get('attorneys/', params=params) 