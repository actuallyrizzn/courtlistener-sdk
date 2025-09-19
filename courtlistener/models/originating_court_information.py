"""
Originating Court Information model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class OriginatingCourtInformation(BaseModel):
    """Model representing originating court information."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.court: Optional[str] = data.get('court')
        self.jurisdiction: Optional[str] = data.get('jurisdiction')
        self.description: Optional[str] = data.get('description')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
