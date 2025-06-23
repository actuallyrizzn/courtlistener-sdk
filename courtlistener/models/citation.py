"""Citation model for CourtListener SDK."""

from .base import BaseModel


class Citation(BaseModel):
    """Model for citation data."""
    
    def _parse_data(self):
        """Parse citation data."""
        super()._parse_data() 