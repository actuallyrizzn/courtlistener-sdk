"""Documents API module for CourtListener SDK."""

from typing import Dict, Any, Optional
from ..utils.filters import build_filters
from ..utils.validators import validate_id
from ..models.base import BaseModel


class Document(BaseModel):
    """Model for document data."""
    pass


class DocumentsAPI:
    """API client for documents functionality."""
    
    def __init__(self, client):
        self.client = client
    
    def list_documents(self, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """List documents with optional filtering."""
        params = filters or {}
        return self.client.get('recap-documents/', params=params)
    
    def get_document(self, document_id: int) -> Document:
        """Get a specific document by ID."""
        validate_id(document_id)
        data = self.client.get(f'recap-documents/{document_id}/')
        return Document(data) 