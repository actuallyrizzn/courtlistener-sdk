"""Audio API module for CourtListener SDK."""

from typing import Dict, Any, Optional, List
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Audio(BaseModel):
    """Model for audio data."""
    pass


class AudioAPI:
    """Audio API endpoints."""
    
    def __init__(self, client):
        self.client = client
    
    def list_audio(self, page: int = 1, q: str = None, **filters) -> List[Audio]:
        """List audio files."""
        try:
            params = {"page": page}
            if q:
                params["q"] = q
            params.update(filters)
            
            response = self.client._make_request("GET", "/audio/", params=params)
            return [Audio(item) for item in response.get("results", [])]
        except Exception as e:
            # Audio endpoint might be restricted in some cases
            self.client.logger.warning(f"Audio endpoint may be restricted: {e}")
            return []
    
    def get_audio(self, audio_id: int) -> Optional[Audio]:
        """Get a specific audio file."""
        try:
            response = self.client._make_request("GET", f"/audio/{audio_id}/")
            return Audio(response)
        except Exception as e:
            self.client.logger.warning(f"Could not fetch audio {audio_id}: {e}")
            return None
    
    def search_audio(self, q: str, page: int = 1, **filters) -> List[Audio]:
        """Search audio files."""
        return self.list_audio(page=page, q=q, **filters) 