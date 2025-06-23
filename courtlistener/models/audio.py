"""Audio model for CourtListener SDK."""

from .base import BaseModel


class Audio(BaseModel):
    """Model for audio data."""
    
    def _parse_data(self):
        """Parse audio data."""
        super()._parse_data()
        for field in [
            'id', 'docket', 'docket_entry', 'source', 'duration', 'local_path', 'file_path', 'file_url',
            'filepath_local', 'date', 'absolute_url', 'resource_uri']:
            if not hasattr(self, field):
                setattr(self, field, None)
        
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
        return bool(self.local_path or self.file_path or self.file_url or self.filepath_local)
    
    @property
    def docket_entry(self) -> int:
        """Get docket entry ID."""
        return getattr(self, '_docket_entry', None)
    
    @property
    def duration_formatted(self) -> str:
        """Get formatted duration string."""
        duration = self.duration or 0
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"0:{minutes:02d}:{seconds:02d}"
    
    def __repr__(self) -> str:
        """String representation of the audio."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket = getattr(self, 'docket', None)
            source = getattr(self, 'source', 'None')
            duration = getattr(self, 'duration', None)
            return f"<Audio(id={self.id}, docket={docket}, source='{source}', duration={duration})>"
        return f"<Audio()>"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            source = getattr(self, 'source', 'None')
            duration = getattr(self, 'duration', None)
            return f"{class_name}(id={self.id}, source='{source}', duration={duration})"
        return f"{class_name}()" 