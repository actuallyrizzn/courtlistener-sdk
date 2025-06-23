"""Judge model for CourtListener SDK."""

from .base import BaseModel


class Judge(BaseModel):
    """Model for judge data."""
    
    def _parse_data(self):
        """Parse judge data."""
        super()._parse_data()
        
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
        return bool(
            getattr(self, 'date_died', None) or
            getattr(self, 'deceased', False) or
            self._data.get('is_deceased', False)
        )
    
    @property
    def full_name(self) -> str:
        """Get formatted full name."""
        parts = []
        if hasattr(self, 'name_first') and self.name_first:
            parts.append(self.name_first)
        if hasattr(self, 'name_middle') and self.name_middle:
            parts.append(self.name_middle)
        if hasattr(self, 'name_last') and self.name_last:
            parts.append(self.name_last)
        if hasattr(self, 'name_suffix') and self.name_suffix:
            parts.append(self.name_suffix)
        
        if parts:
            return ' '.join(parts)
        elif hasattr(self, 'name') and self.name:
            return self.name
        else:
            return ''
    
    @property
    def date_dob(self) -> str:
        """Get date of birth."""
        return self._data.get('birthday', self._data.get('date_dob', None))
    
    def __repr__(self) -> str:
        """String representation of the judge."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            return f"{class_name}(id={self.id}, name='{name}')"
        return f"{class_name}()" 