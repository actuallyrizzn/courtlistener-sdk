"""Judge model for CourtListener SDK."""

from .base import BaseModel


class Judge(BaseModel):
    """Model for judge data."""
    
    def _parse_data(self):
        """Parse judge data."""
        super()._parse_data()
        for field in [
            'id', 'name', 'name_first', 'name_last', 'name_middle', 'name_suffix', 'birthday', 'date_dob', 'date_died',
            'court', 'positions', 'absolute_url', 'resource_uri', 'deceased']:
            if not hasattr(self, field):
                setattr(self, field, None)
        
        # Parse dates
        if hasattr(self, 'date_dob'):
            self.date_dob = self._parse_datetime(self.date_dob)
        if hasattr(self, 'date_died'):
            self.date_died = self._parse_datetime(self.date_died)
        
        # Map API fields to expected properties
        if hasattr(self, 'name_first') and hasattr(self, 'name_last'):
            self.name_first = self.name_first
            self.name_last = self.name_last
        elif hasattr(self, 'name') and not hasattr(self, 'name_first'):
            # Try to split full name
            name_parts = self.name.split()
            if len(name_parts) >= 2:
                self.name_first = name_parts[0]
                self.name_last = name_parts[-1]
            else:
                self.name_first = None
                self.name_last = self.name
        else:
            self.name_first = None
            self.name_last = None
    
    @property
    def is_deceased(self) -> bool:
        """Check if judge is deceased."""
        return bool(self.date_died or self.deceased)
    
    @property
    def full_name(self) -> str:
        """Get formatted full name."""
        parts = []
        if self.name_first:
            parts.append(self.name_first)
        if self.name_middle:
            parts.append(self.name_middle)
        if self.name_last:
            parts.append(self.name_last)
        if self.name_suffix:
            parts.append(self.name_suffix)
        return ' '.join([p for p in parts if p]) or self.name or ''
    
    @property
    def date_dob(self) -> str:
        """Get date of birth."""
        return getattr(self, '_date_dob', None) or getattr(self, 'birthday', None)
    
    def __repr__(self) -> str:
        """String representation of the judge."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            return f"<Judge(id={self.id}, name='{name}')>"
        return f"<Judge()>"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            return f"Judge(id={self.id}, name='{name}')"
        return f"{class_name}()" 