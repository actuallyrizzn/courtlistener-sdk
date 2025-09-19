"""
FJC Integrated Database model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class FJCIntegratedDatabase(BaseModel):
    """Model representing FJC integrated database records."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.person: Optional[str] = data.get('person')
        self.court: Optional[str] = data.get('court')
        self.position: Optional[str] = data.get('position')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
