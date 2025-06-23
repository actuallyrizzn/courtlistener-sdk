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
    
    def list_courts(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List courts with optional filtering."""
        params = filters or {}
        return self.client.get('courts/', params=params)
    
    def get_court(self, court_id: str) -> Court:
        """Get a specific court by ID."""
        data = self.client.get(f'courts/{court_id}/')
        return Court(data) 