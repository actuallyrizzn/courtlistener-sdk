"""
Agreement model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class Agreement(BaseModel):
    """Model representing an agreement from financial disclosures."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.financial_disclosure: Optional[str] = data.get('financial_disclosure')
        self.judge: Optional[str] = data.get('judge')
        self.description: Optional[str] = data.get('description')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
