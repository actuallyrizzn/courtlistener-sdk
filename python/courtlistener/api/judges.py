"""
Judges API client for CourtListener.
"""

from typing import List, Optional, Dict, Any
from ..models.judge import Judge
from ..exceptions import NotFoundError, APIError
from .base import BaseAPI


class JudgesAPI(BaseAPI):
    """API client for judges/people endpoints."""
    
    def __init__(self, client):
        self.client = client
        self.base_url = f"{client.config.base_url}/people"
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "people/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Judge
    
    def list_judges(self, page: int = 1, **filters) -> List[Judge]:
        """
        List judges/people.
        
        Args:
            page: Page number for pagination
            **filters: Additional filters to apply
            
        Returns:
            List of Judge objects
        """
        params = {"page": page, **filters}
        response = self.client._make_request("GET", self.base_url, params=params)
        
        judges = []
        for judge_data in response.get("results", []):
            judges.append(Judge(judge_data))
        
        return judges
    
    def get_judge(self, judge_id: int) -> Judge:
        """
        Get a specific judge by ID.
        
        Args:
            judge_id: Judge ID
            
        Returns:
            Judge object
            
        Raises:
            NotFoundError: If judge not found
        """
        url = f"{self.base_url}/{judge_id}"
        response = self.client._make_request("GET", url)
        return Judge(response)
    
    def search_judges(self, q: str, page: int = 1, **filters) -> List[Judge]:
        """
        Search for judges.
        
        Args:
            q: Search query
            page: Page number for pagination
            **filters: Additional filters to apply
            
        Returns:
            List of Judge objects
        """
        params = {"q": q, "page": page, **filters}
        response = self.client._make_request("GET", self.base_url, params=params)
        
        judges = []
        for judge_data in response.get("results", []):
            judges.append(Judge(judge_data))
        
        return judges 