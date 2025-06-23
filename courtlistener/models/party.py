"""Party model for CourtListener SDK."""

from .base import BaseModel


class Party(BaseModel):
    """Model for party data."""
    
    def _parse_data(self):
        """Parse party data."""
        super()._parse_data()
        
        # Parse related models if they exist
        if hasattr(self, 'attorneys') and isinstance(self.attorneys, list):
            from .attorney import Attorney
            self.attorneys = self._parse_list(self.attorneys, Attorney) 