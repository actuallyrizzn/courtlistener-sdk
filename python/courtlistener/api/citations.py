"""Citations API module for CourtListener SDK."""

from typing import Dict, Any, Optional, List
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel
from .base import BaseAPI


class Citation(BaseModel):
    """Model for citation data."""
    pass


class CitationsAPI(BaseAPI):
    """API client for citations functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "citations/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Citation
    
    def get_citations_by_opinion(self, opinion_id: int) -> Dict[str, Any]:
        """Get citations by a specific opinion."""
        validate_id(opinion_id)
        return self.client.get('opinions-cited/', params={'citing_opinion': opinion_id})
    
    def get_cited_by_opinions(self, opinion_id: int) -> Dict[str, Any]:
        """Get opinions that cite a specific opinion."""
        validate_id(opinion_id)
        return self.client.get('opinions-cited/', params={'cited_opinion': opinion_id})
    
    def lookup_citations(self, text: str) -> List[Dict[str, Any]]:
        """Look up citations in text."""
        data = {'text': text}
        return self.client.post('citation-lookup/', json_data=data)

    def list_citations(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('citations/', params=params)

    def search_citations(self, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['page'] = page
        return self.client.get('citations/', params=params) 