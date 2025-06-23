"""Judge model for CourtListener SDK."""

from .base import BaseModel


class Judge(BaseModel):
    """Model for judge data."""
    
    def _parse_data(self):
        """Parse judge data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'birthday'):
            self.birthday = self._parse_date(self.birthday)
        if hasattr(self, 'date_died'):
            self.date_died = self._parse_date(self.date_died) 