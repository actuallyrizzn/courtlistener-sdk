"""Parties API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel
from .base import BaseAPI


class Party(BaseModel):
    """Model for party data."""
    pass


class PartiesAPI(BaseAPI):
    """API client for parties functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "parties/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Party
    
    def list_parties(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List parties with optional filtering."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('parties/', params=params)
    
    def get_party(self, party_id: int) -> Party:
        """Get a specific party by ID."""
        validate_id(party_id)
        data = self.client.get(f'parties/{party_id}/')
        return Party(data)

    def search_parties(self, q: str, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['q'] = q
        params['page'] = page
        return self.client.get('parties/', params=params) 