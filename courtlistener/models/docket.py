"""Docket model for CourtListener SDK."""

from .base import BaseModel


class Docket(BaseModel):
    """Model for docket data."""
    
    def _parse_data(self):
        """Parse docket data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed)
        
        # Parse related models if they exist
        if hasattr(self, 'court') and isinstance(self.court, dict):
            from .court import Court
            self.court = self._parse_related_model(self.court, Court) 