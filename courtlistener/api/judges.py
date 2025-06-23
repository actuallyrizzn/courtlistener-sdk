"""Judges API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Judge(BaseModel):
    """Model for judge data."""
    pass


class JudgesAPI:
    """API client for judges functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_judges(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List judges with optional filtering, pagination, and search."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('judges/', params=params)
    
    def get_judge(self, judge_id: int) -> Judge:
        """Get a specific judge by ID."""
        validate_id(judge_id)
        data = self.client.get(f'judges/{judge_id}/')
        return Judge(data)

    def search_judges(self, q: str, page: int = 1, **filters) -> Dict[str, Any]:
        """Search judges by query string."""
        params = filters.copy() if filters else {}
        params['q'] = q
        params['page'] = page
        return self.client.get('judges/', params=params) 
