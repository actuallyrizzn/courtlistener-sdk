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
    
    def list_attorneys(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List attorneys with optional filtering."""
        params = filters or {}
        return self.client.get('attorneys/', params=params)
    
    def get_attorney(self, attorney_id: int) -> Attorney:
        """Get a specific attorney by ID."""
        validate_id(attorney_id)
        data = self.client.get(f'attorneys/{attorney_id}/')
        return Attorney(data) 