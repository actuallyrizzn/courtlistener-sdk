"""
Retention Event model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class RetentionEvent(BaseModel):
    """Model representing a data retention event."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.event_type: Optional[str] = data.get('event_type')
        self.description: Optional[str] = data.get('description')
        self.date: Optional[str] = data.get('date')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
