"""Audio model for CourtListener SDK."""

from .base import BaseModel


class Audio(BaseModel):
    """Model for audio data."""
    
    def _parse_data(self):
        """Parse audio data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date'):
            self.date = self._parse_date(self.date) 