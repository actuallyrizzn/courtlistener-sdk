"""Audio model for CourtListener SDK."""

from .base import BaseModel


class Audio(BaseModel):
    """Model for audio data."""
    
    def _parse_data(self):
        """Parse audio data."""
        super()._parse_data()
        
        # Map API fields to expected properties
        if hasattr(self, 'docket_id') and not hasattr(self, 'docket'):
            self.docket = self.docket_id
        elif not hasattr(self, 'docket'):
            self.docket = None
        
        # Parse dates
        if hasattr(self, 'date'):
            self.date = self._parse_date(self.date)
    
    @property
    def has_local_file(self) -> bool:
        """Check if audio has a local file."""
        return bool(
            getattr(self, 'local_path', None) or 
            getattr(self, 'file_path', None) or
            getattr(self, 'file_url', None)
        )
    
    @property
    def docket_entry(self) -> int:
        """Get docket entry ID."""
        return getattr(self, 'docket_entry_id', None)
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        duration = getattr(self, 'duration', 0)
        if not duration:
            return '0:00'
        
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def __repr__(self) -> str:
        """String representation of the audio."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            source = getattr(self, 'source', 'unknown')
            duration = getattr(self, 'duration', 0)
            return f"{class_name}(id={self.id}, source='{source}', duration={duration})"
        return f"{class_name}()" 