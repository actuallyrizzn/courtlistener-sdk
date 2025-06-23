"""Parties API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Party(BaseModel):
    """Model for party data."""
    pass


class PartiesAPI:
    """API client for parties functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_parties(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List parties with optional filtering."""
        params = filters or {}
        return self.client.get('parties/', params=params)
    
    def get_party(self, party_id: int) -> Party:
        """Get a specific party by ID."""
        validate_id(party_id)
        data = self.client.get(f'parties/{party_id}/')
        return Party(data) 