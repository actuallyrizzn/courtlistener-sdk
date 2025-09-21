"""
Source model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class Source(BaseModel):
    """Model representing a data source."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.name: Optional[str] = data.get('name')
        self.type: Optional[str] = data.get('type')
        self.url: Optional[str] = data.get('url')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
