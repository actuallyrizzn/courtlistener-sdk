"""
Disclosure Position model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class DisclosurePosition(BaseModel):
    """Model representing a disclosure position from financial disclosures."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.financial_disclosure: Optional[str] = data.get('financial_disclosure')
        self.judge: Optional[str] = data.get('judge')
        self.position: Optional[str] = data.get('position')
        self.organization: Optional[str] = data.get('organization')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
