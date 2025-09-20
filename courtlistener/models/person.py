"""
Person model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class Person(BaseModel):
    """Model representing a person in the legal system."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        id_value = data.get('id')
        if id_value is not None:
            try:
                self.id: Optional[int] = int(id_value)
            except (ValueError, TypeError):
                self.id: Optional[int] = None
        else:
            self.id: Optional[int] = None
        self.name: Optional[str] = data.get('name')
        self.court: Optional[str] = data.get('court')
        self.position: Optional[str] = data.get('position')
        self.birthday: Optional[str] = data.get('birthday')
        self.education: Optional[str] = data.get('education')
        self.political_affiliation: Optional[str] = data.get('political_affiliation')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
