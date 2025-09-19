"""
Opinions API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, Iterator, List
from ..utils.filters import build_filters, build_date_range_filter
from ..utils.pagination import PageIterator
from ..utils.validators import validate_id
from ..models.base import BaseModel
from ..models.opinion import Opinion
from .base import BaseAPI


class OpinionsAPI(BaseAPI):
    """API client for opinions functionality."""
    
    def __init__(self, client):
        """Initialize Opinions API client."""
        self.client = client
        self.base_url = f"{client.config.base_url}/opinions"
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "opinions/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Opinion
    
    def list_opinions(self, page: int = 1, q: str = None, **filters) -> List[Opinion]:
        """List opinions."""
        params = {"page": page}
        if q:
            params["q"] = q
        params.update(filters)
        
        response = self.client._make_request("GET", "/opinions/", params=params)
        return [Opinion(item) for item in response.get("results", [])]
    
    def get_opinion(self, opinion_id: int) -> Opinion:
        """Get a specific opinion by ID."""
        url = f"{self.base_url}/{opinion_id}"
        response = self.client._make_request("GET", url)
        return Opinion(response)

    def search_opinions(self, q: str, page: int = 1, **filters) -> List[Opinion]:
        """Search opinions."""
        return self.list_opinions(page=page, q=q, **filters) 