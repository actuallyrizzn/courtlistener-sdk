"""
School model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class School(BaseModel):
    """Model representing an educational institution."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.name: Optional[str] = data.get('name')
        self.type: Optional[str] = data.get('type')
        self.location: Optional[str] = data.get('location')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
