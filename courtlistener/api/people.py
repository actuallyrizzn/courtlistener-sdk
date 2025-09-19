"""
People API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class PeopleAPI(BaseAPI):
    """API for accessing the people database."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "people/"
    
    def list(
        self,
        name: Optional[str] = None,
        name__icontains: Optional[str] = None,
        court: Optional[str] = None,
        position_type: Optional[str] = None,
        active: Optional[bool] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List people records.
        
        Args:
            name: Filter by exact name match
            name__icontains: Filter by partial name match (case-insensitive)
            court: Filter by court ID or slug
            position_type: Filter by position type (Judge, Justice, Attorney)
            active: Filter by active status
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of people
        """
        params = {}
        if name is not None:
            params['name'] = name
        if name__icontains is not None:
            params['name__icontains'] = name__icontains
        if court is not None:
            params['court'] = court
        if position_type is not None:
            params['position_type'] = position_type
        if active is not None:
            params['active'] = active
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, person_id: int) -> Dict[str, Any]:
        """
        Get a specific person by ID.
        
        Args:
            person_id: Person ID
        
        Returns:
            Person data
        """
        return self.client.get(f"{self.endpoint}{person_id}/")
    
    def paginate(
        self,
        name: Optional[str] = None,
        name__icontains: Optional[str] = None,
        court: Optional[str] = None,
        position_type: Optional[str] = None,
        active: Optional[bool] = None,
        **kwargs
    ):
        """
        Get paginated people records.
        
        Args:
            name: Filter by exact name match
            name__icontains: Filter by partial name match (case-insensitive)
            court: Filter by court ID or slug
            position_type: Filter by position type (Judge, Justice, Attorney)
            active: Filter by active status
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for people records
        """
        params = {}
        if name is not None:
            params['name'] = name
        if name__icontains is not None:
            params['name__icontains'] = name__icontains
        if court is not None:
            params['court'] = court
        if position_type is not None:
            params['position_type'] = position_type
        if active is not None:
            params['active'] = active
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
