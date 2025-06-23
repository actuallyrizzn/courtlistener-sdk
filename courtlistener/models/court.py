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
        
        for field in [
            'id', 'name', 'name_abbreviation', 'short_name', 'jurisdiction', 'slug', 'url', 'start_date', 'end_date',
            'absolute_url', 'resource_uri', 'defunct']:
            if not hasattr(self, field):
                setattr(self, field, None)
    
    @property
    def is_defunct(self) -> bool:
        """Check if court is defunct."""
        return bool(self.end_date or self.defunct)
    
    @property
    def short_name(self) -> str:
        """Get short name of the court."""
        return getattr(self, '_short_name', None) or getattr(self, 'name_abbreviation', None)
    
    def __repr__(self) -> str:
        """String representation of the court."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            short_name = self.short_name
            return f"<Court(id={self.id}, name='{name}', short_name='{short_name}')>"
        return f"<Court()>"
    
    def __str__(self) -> str:
        """String representation of the court."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            short_name = self.short_name
            return f"{class_name}(id={self.id}, name='{name}', short_name='{short_name}')"
        return f"{class_name}()" 