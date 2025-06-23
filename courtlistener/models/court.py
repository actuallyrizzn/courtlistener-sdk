"""Court model for CourtListener SDK."""

from .base import BaseModel


class Court(BaseModel):
    """Model for court data."""
    
    def _parse_data(self):
        """Parse court data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'start_date'):
            self.start_date = self._parse_datetime(self.start_date)
        if hasattr(self, 'end_date'):
            self.end_date = self._parse_datetime(self.end_date)
        
        # Map API fields to expected properties
        if hasattr(self, 'full_name') and not hasattr(self, 'name'):
            self.name = self.full_name
        elif not hasattr(self, 'name'):
            self.name = None
    
    @property
    def is_defunct(self) -> bool:
        """Check if court is defunct."""
        return bool(
            getattr(self, 'end_date', None) or
            getattr(self, 'defunct', False) or
            self._data.get('is_defunct', False)
        )
    
    @property
    def short_name(self) -> str:
        """Get short name of the court."""
        return self._data.get('name_abbreviation', self._data.get('short_name', None))
    
    def __repr__(self) -> str:
        """String representation of the court."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            short_name = getattr(self, 'short_name', getattr(self, 'name_abbreviation', 'Unknown'))
            return f"{class_name}(id={self.id}, name='{name}', short_name='{short_name}')"
        return f"{class_name}()" 