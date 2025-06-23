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
    
    def list_documents(self, page: int = 1, q: str = None, **filters) -> Dict[str, Any]:
        """List documents with optional filtering."""
        params = filters.copy() if filters else {}
        params['page'] = page
        if q:
            params['q'] = q
        return self.client.get('documents/', params=params)
    
    def get_document(self, document_id: int) -> Document:
        """Get a specific document by ID."""
        validate_id(document_id)
        data = self.client.get(f'recap-documents/{document_id}/')
        return Document(data)

    def search_documents(self, q: str, page: int = 1, **filters) -> Dict[str, Any]:
        params = filters.copy() if filters else {}
        params['q'] = q
        params['page'] = page
        return self.client.get('documents/', params=params) 