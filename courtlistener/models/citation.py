"""Citation model for CourtListener SDK."""

from .base import BaseModel


class Citation(BaseModel):
    """Model for citation data."""
    
    def _parse_data(self):
        """Parse citation data."""
        super()._parse_data()
        
        # Map API fields to expected properties
        if hasattr(self, 'reporter') and not hasattr(self, 'volume'):
            # Extract volume from reporter if possible
            self.volume = None
        elif not hasattr(self, 'volume'):
            self.volume = None
    
    @property
    def citation_string(self) -> str:
        """Get formatted citation string."""
        parts = []
        if hasattr(self, 'volume') and self.volume:
            parts.append(str(self.volume))
        if hasattr(self, 'reporter') and self.reporter:
            parts.append(self.reporter)
        if hasattr(self, 'page') and self.page:
            parts.append(str(self.page))
        
        if parts:
            return ' '.join(parts)
        elif hasattr(self, 'citation') and self.citation:
            return self.citation
        else:
            return ''
    
    @property
    def reporter(self) -> str:
        """Get reporter name."""
        return self._data.get('reporter_name', self._data.get('reporter', None))
    
    @property
    def is_federal(self) -> bool:
        """Check if this is a federal citation."""
        reporter = getattr(self, 'reporter', '').lower()
        return 'u.s.' in reporter or 'f.' in reporter or 'f.2d' in reporter or 'f.3d' in reporter
    
    def __repr__(self) -> str:
        """String representation of the citation."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            citation = getattr(self, 'citation', 'Unknown')
            year = getattr(self, 'year', 'Unknown')
            return f"{class_name}(id={self.id}, citation='{citation}', year={year})"
        return f"{class_name}()" 