"""
Alert model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class Alert(BaseModel):
    """Model representing a search or docket alert."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.name: Optional[str] = data.get('name')
        self.query: Optional[str] = data.get('query')
        self.rate: Optional[str] = data.get('rate')
        self.alert_type: Optional[str] = data.get('alert_type')
        self.webhook_url: Optional[str] = data.get('webhook_url')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
