"""Attorney model for CourtListener SDK."""

from .base import BaseModel


class Attorney(BaseModel):
    """Model for attorney data."""
    
    def _parse_data(self):
        """Parse attorney data."""
        super()._parse_data() 