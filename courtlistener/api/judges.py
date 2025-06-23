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
    
    def list_judges(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List judges with optional filtering."""
        params = filters or {}
        return self.client.get('judges/', params=params)
    
    def get_judge(self, judge_id: int) -> Judge:
        """Get a specific judge by ID."""
        validate_id(judge_id)
        data = self.client.get(f'judges/{judge_id}/')
        return Judge(data) 