"""
Tests for RecapDocument model.
"""

import pytest
from courtlistener.models.recap_document import RecapDocument


class TestRecapDocument:
    """Test cases for RecapDocument model."""
    
    def test_recap_document_creation(self):
        """Test creating a RecapDocument instance."""
        data = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "docket_entry": "https://api.courtlistener.com/api/rest/v4/docket-entries/456/",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "file_url": "https://example.com/document.pdf",
            "file_size": 1024,
            "file_type": "pdf",
            "is_available": True,
            "page_count": 10,
            "attachment_number": 1,
            "description": "Test document",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/recap-documents/1/",
            "absolute_url": "https://www.courtlistener.com/recap/document/1/"
        }
        
        doc = RecapDocument(data)
        
        assert doc.id == 1
        assert doc.docket == "https://api.courtlistener.com/api/rest/v4/dockets/123/"
        assert doc.docket_entry == "https://api.courtlistener.com/api/rest/v4/docket-entries/456/"
        assert doc.court == "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        assert doc.file_url == "https://example.com/document.pdf"
        assert doc.file_size == 1024
        assert doc.file_type == "pdf"
        assert doc.is_available is True
        assert doc.page_count == 10
        assert doc.attachment_number == 1
        assert doc.description == "Test document"
        assert doc.date_created == "2023-01-01T00:00:00Z"
        assert doc.date_modified == "2023-01-02T00:00:00Z"
        assert doc.resource_uri == "https://api.courtlistener.com/api/rest/v4/recap-documents/1/"
        assert doc.absolute_url == "https://www.courtlistener.com/recap/document/1/"
    
    def test_recap_document_with_none_values(self):
        """Test creating a RecapDocument with None values."""
        data = {
            "id": 1,
            "docket": None,
            "docket_entry": None,
            "court": None,
            "file_url": None,
            "file_size": None,
            "file_type": None,
            "is_available": None,
            "page_count": None,
            "attachment_number": None,
            "description": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        doc = RecapDocument(data)
        
        assert doc.id == 1
        assert doc.docket is None
        assert doc.docket_entry is None
        assert doc.court is None
        assert doc.file_url is None
        assert doc.file_size is None
        assert doc.file_type is None
        assert doc.is_available is None
        assert doc.page_count is None
        assert doc.attachment_number is None
        assert doc.description is None
        assert doc.date_created is None
        assert doc.date_modified is None
        assert doc.resource_uri is None
        assert doc.absolute_url is None
