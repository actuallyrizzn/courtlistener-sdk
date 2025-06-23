"""Opinion model for CourtListener SDK."""

from .base import BaseModel


class Opinion(BaseModel):
    """Model for opinion data."""
    
    def _parse_data(self):
        """Parse opinion data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed) 