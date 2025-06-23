"""Court model for CourtListener SDK."""

from .base import BaseModel


class Court(BaseModel):
    """Model for court data."""
    
    def _parse_data(self):
        """Parse court data."""
        super()._parse_data() 