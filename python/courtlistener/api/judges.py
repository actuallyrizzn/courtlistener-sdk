"""
Judges API client for CourtListener.
"""

from typing import List, Optional, Dict, Any, Union
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
    
    def list(self, page: int = 1, **filters) -> List[Judge]:
        """
        List judges/people with optional filtering and pagination.
        
        Standard method name for listing resources. This is the preferred method.
        
        Args:
            page: Page number (default: 1)
            **filters: Additional filter parameters
        
        Returns:
            List of Judge objects
        """
        return self.list_judges(page=page, **filters)
    
    def get(self, judge_id: Union[int, str]) -> Judge:
        """
        Get a specific judge by ID.
        
        Standard method name for getting a resource. This is the preferred method.
        
        Args:
            judge_id: Judge ID
        
        Returns:
            Judge object
        
        Raises:
            NotFoundError: If judge not found
        """
        return self.get_judge(int(judge_id))
    
    def search(self, q: str, page: int = 1, **filters) -> List[Judge]:
        """
        Search for judges.
        
        Standard method name for searching resources. This is the preferred method.
        
        Args:
            q: Search query
            page: Page number (default: 1)
            **filters: Additional filter parameters
        
        Returns:
            List of Judge objects
        """
        return self.search_judges(q=q, page=page, **filters)
    
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