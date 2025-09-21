"""Citation model for CourtListener SDK."""

from .base import BaseModel


class Citation(BaseModel):
    """Model for citation data."""
    
    def _parse_data(self):
        """Parse citation data."""
        super()._parse_data()
        for field in [
            'id', 'volume', 'reporter', 'page', 'citation', 'year', 'reporter_name', 'type',
            'absolute_url', 'resource_uri']:
            if not hasattr(self, field):
                setattr(self, field, None)
        # Set _reporter if reporter is present
        if hasattr(self, 'reporter'):
            self._reporter = getattr(self, 'reporter')
    
    @property
    def citation_string(self) -> str:
        """Get formatted citation string."""
        parts = []
        if self.volume:
            parts.append(str(self.volume))
        if self.reporter:
            parts.append(self.reporter)
        if self.page:
            parts.append(str(self.page))
        
        if parts:
            return ' '.join(parts)
        elif self._data.get('citation'):
            return self._data.get('citation')
        else:
            return ''
    
    @property
    def reporter(self) -> str:
        """Get reporter name."""
        return self._data.get('reporter', None)
    
    @property
    def volume(self) -> int:
        """Get volume number."""
        return self._data.get('volume', None)
    
    @property
    def page(self) -> int:
        """Get page number."""
        return self._data.get('page', None)
    
    @property
    def type(self) -> str:
        """Get citation type."""
        return self._data.get('type', None)
    
    @property
    def year(self) -> int:
        """Get year."""
        return self._data.get('year', None)
    
    @property
    def absolute_url(self) -> str:
        """Get absolute URL."""
        return self._data.get('absolute_url', None)
    
    @property
    def resource_uri(self) -> str:
        """Get resource URI."""
        return self._data.get('resource_uri', None)
    
    @property
    def citation(self) -> str:
        """Get citation string."""
        return self.citation_string
    
    @property
    def is_federal(self) -> bool:
        """Check if this is a federal citation."""
        if self.type == 'federal':
            return True
        reporter = (self.reporter or '').lower()
        return 'u.s.' in reporter or 'f.' in reporter or 'f.2d' in reporter or 'f.3d' in reporter
    
    @property
    def is_state(self) -> bool:
        """Check if this is a state citation."""
        return self.type == 'state'
    
    def __repr__(self) -> str:
        """String representation of the citation."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            citation = getattr(self, 'citation', 'Unknown')
            year = getattr(self, 'year', 'Unknown')
            return f"{class_name}(id={self.id}, citation='{citation}', year={year})"
        return f"{class_name}()"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Citation':
        """Create Citation instance from dictionary."""
        return cls(data) 