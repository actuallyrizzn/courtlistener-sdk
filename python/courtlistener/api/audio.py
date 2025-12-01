"""Audio API module for CourtListener SDK."""

from typing import Dict, Any, Optional, List, Union
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel
from .base import BaseAPI


class Audio(BaseModel):
    """Model for audio data."""
    pass


class AudioAPI(BaseAPI):
    """Audio API endpoints."""
    
    def __init__(self, client):
        self.client = client
    
    def _get_endpoint(self) -> str:
        """Get the API endpoint for this module."""
        return "audio/"
    
    def _get_model_class(self):
        """Get the model class associated with this API."""
        return Audio
    
    def list(self, page: int = 1, q: str = None, **filters) -> List[Audio]:
        """
        List audio files with optional filtering and pagination.
        
        Standard method name for listing resources. This is the preferred method.
        
        Args:
            page: Page number (default: 1)
            q: Search query (optional)
            **filters: Additional filter parameters
        
        Returns:
            List of Audio objects
        """
        return self.list_audio(page=page, q=q, **filters)
    
    def get(self, audio_id: Union[int, str]) -> Optional[Audio]:
        """
        Get a specific audio file by ID.
        
        Standard method name for getting a resource. This is the preferred method.
        
        Args:
            audio_id: Audio ID
        
        Returns:
            Audio object or None if not found
        """
        return self.get_audio(int(audio_id))
    
    def search(self, q: str, page: int = 1, **filters) -> List[Audio]:
        """
        Search audio files.
        
        Standard method name for searching resources. This is the preferred method.
        
        Args:
            q: Search query
            page: Page number (default: 1)
            **filters: Additional filter parameters
        
        Returns:
            List of Audio objects
        """
        return self.search_audio(q=q, page=page, **filters)
    
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