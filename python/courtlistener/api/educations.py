"""
Educations API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class EducationsAPI(BaseAPI):
    """API for accessing education records data."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "educations/"
    
    def list(
        self,
        person: Optional[int] = None,
        school: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List education records.
        
        Args:
            person: Filter by person ID
            school: Filter by school ID
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of education records
        """
        params = {}
        if person is not None:
            params['person'] = person
        if school is not None:
            params['school'] = school
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, education_id: int) -> Dict[str, Any]:
        """
        Get a specific education record by ID.
        
        Args:
            education_id: Education record ID
        
        Returns:
            Education record data
        """
        return self.client.get(f"{self.endpoint}{education_id}/")
    
    def paginate(
        self,
        person: Optional[int] = None,
        school: Optional[int] = None,
        **kwargs
    ):
        """
        Get paginated education records.
        
        Args:
            person: Filter by person ID
            school: Filter by school ID
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for education records
        """
        params = {}
        if person is not None:
            params['person'] = person
        if school is not None:
            params['school'] = school
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
