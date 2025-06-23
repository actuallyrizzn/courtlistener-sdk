"""Audio API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Audio(BaseModel):
    """Model for audio data."""
    pass


class AudioAPI:
    """API client for audio functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_audio(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List audio recordings with optional filtering."""
        params = filters or {}
        return self.client.get('audio/', params=params)
    
    def get_audio(self, audio_id: int) -> Audio:
        """Get a specific audio recording by ID."""
        validate_id(audio_id)
        data = self.client.get(f'audio/{audio_id}/')
        return Audio(data) 