"""
Opinion Cited model for CourtListener SDK.
"""

from typing import Optional, Dict, Any
from .base import BaseModel


class OpinionCited(BaseModel):
    """Model representing a citation relationship between opinions."""
    
    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.id: Optional[int] = data.get('id')
        self.citing_opinion: Optional[str] = data.get('citing_opinion')
        self.cited_opinion: Optional[str] = data.get('cited_opinion')
        self.date_created: Optional[str] = data.get('date_created')
        self.date_modified: Optional[str] = data.get('date_modified')
        self.resource_uri: Optional[str] = data.get('resource_uri')
        self.absolute_url: Optional[str] = data.get('absolute_url')
