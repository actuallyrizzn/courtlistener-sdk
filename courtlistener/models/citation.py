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
        elif self.citation:
            return self.citation
        else:
            return ''
    
    @property
    def reporter(self) -> str:
        """Get reporter name."""
        return getattr(self, '_reporter', None)
    
    @property
    def is_federal(self) -> bool:
        """Check if this is a federal citation."""
        reporter = (self.reporter or '').lower()
        return 'u.s.' in reporter or 'f.' in reporter or 'f.2d' in reporter or 'f.3d' in reporter
    
    def __repr__(self) -> str:
        """String representation of the citation."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            citation = getattr(self, 'citation', 'Unknown')
            year = getattr(self, 'year', 'Unknown')
            return f"{class_name}(id={self.id}, citation='{citation}', year={year})"
        return f"{class_name}()" 