"""Document model for CourtListener SDK."""

from .base import BaseModel


class Document(BaseModel):
    """Model for document data."""
    
    def _parse_data(self):
        """Parse document data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed) 