"""
RECAP Document model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class RecapDocument(BaseModel):
    """Model representing a RECAP document."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.docket: Optional[str] = data.get('docket')
        self.docket_entry: Optional[str] = data.get('docket_entry')
        self.court: Optional[str] = data.get('court')
        self.file_url: Optional[str] = data.get('file_url')
        self.file_size: Optional[int] = data.get('file_size')
        self.file_type: Optional[str] = data.get('file_type')
        self.is_available: Optional[bool] = data.get('is_available')
        self.page_count: Optional[int] = data.get('page_count')
        self.attachment_number: Optional[int] = data.get('attachment_number')
        self.description: Optional[str] = data.get('description')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
