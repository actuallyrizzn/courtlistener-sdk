"""Party model for CourtListener SDK."""

from .base import BaseModel


class Party(BaseModel):
    """Model for party data."""
    
    def _parse_data(self):
        """Parse party data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_terminated'):
            self.date_terminated = self._parse_datetime(self.date_terminated)
        
        # Map API fields to expected properties
        if hasattr(self, 'name') and not hasattr(self, 'name'):
            pass  # Already exists
        elif not hasattr(self, 'name'):
            self.name = None
        
        # Parse related models if they exist
        if hasattr(self, 'attorneys') and isinstance(self.attorneys, list):
            from .attorney import Attorney
            self.attorneys = self._parse_list(self.attorneys, Attorney)
    
    @property
    def is_terminated(self) -> bool:
        """Check if party is terminated."""
        return bool(
            getattr(self, 'date_terminated', None) or
            getattr(self, 'terminated', False) or
            self._data.get('is_terminated', False)
        )
    
    def __repr__(self) -> str:
        """String representation of the party."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            party_type = getattr(self, 'type', 'Unknown')
            return f"{class_name}(id={self.id}, name='{name}', type='{party_type}')"
        return f"{class_name}()" 