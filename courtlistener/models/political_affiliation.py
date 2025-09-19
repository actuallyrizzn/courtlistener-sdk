"""
Political Affiliation model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class PoliticalAffiliation(BaseModel):
    """Model representing a political affiliation."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.person: Optional[str] = data.get('person')
        self.party: Optional[str] = data.get('party')
        self.year: Optional[int] = data.get('year')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
