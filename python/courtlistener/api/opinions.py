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
    
    def list_opinions(self, page: int = 1, q: str = None, filters: dict = None, **kwargs) -> List[Opinion]:
        """List opinions."""
        params = {"page": page}
        if q:
            params["q"] = q
        if filters:
            params.update(filters)
        params.update(kwargs)
        
        response = self.client.get("/opinions/", params=params)
        return [Opinion(item) for item in response.get("results", [])]
    
    def get_opinion(self, opinion_id: int) -> Opinion:
        """Get a specific opinion by ID."""
        response = self.client.get(f"/opinions/{opinion_id}/")
        return Opinion(response)

    def search_opinions(self, q: str, page: int = 1, **filters) -> List[Opinion]:
        """Search opinions."""
        return self.list_opinions(page=page, q=q, **filters)
    
    def get_opinion_cluster(self, cluster_id: int) -> Dict[str, Any]:
        """Get an opinion cluster."""
        response = self.client.get(f"/clusters/{cluster_id}/")
        return response
    
    def list_opinion_clusters(self, page: int = 1, **filters) -> Dict[str, Any]:
        """List opinion clusters."""
        params = {"page": page}
        params.update(filters)
        response = self.client.get("/clusters/", params=params)
        return response
    
    def get_opinions_in_cluster(self, cluster_id: int, **filters) -> List[Opinion]:
        """Get opinions in a cluster."""
        params = {"cluster": cluster_id}
        params.update(filters)
        response = self.client.get("/opinions/", params=params)
        return [Opinion(item) for item in response.get("results", [])]
    
    def get_citations(self, opinion_id: int, **filters) -> Dict[str, Any]:
        """Get citations for an opinion."""
        params = {"citing_opinion": opinion_id}
        params.update(filters)
        response = self.client.get("/opinions-cited/", params=params)
        return response
    
    def get_sub_opinions(self, opinion_id: int) -> List[Opinion]:
        """Get sub-opinions for an opinion."""
        params = {"parent_opinion": opinion_id}
        response = self.client.get("/opinions/", params=params)
        return [Opinion(item) for item in response.get("results", [])] 