"""
Comprehensive tests for the RecapDocument model class.
"""

import pytest
from courtlistener.models.recap_document import RecapDocument


class TestRecapDocument:
    """Test cases for RecapDocument class."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {
            "id": 1,
            "docket": "123",
            "docket_entry": "456",
            "court": "scotus",
            "file_url": "https://example.com/doc.pdf"
        }
        doc = RecapDocument(data)
        assert doc.id == 1
        assert doc.docket == "123"
        assert doc.docket_entry == "456"
        assert doc.court == "scotus"
        assert doc.file_url == "https://example.com/doc.pdf"

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        data = {
            "id": 1,
            "docket": "123",
            "docket_entry": "456",
            "court": "scotus",
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000,
            "file_type": "pdf",
            "is_available": True,
            "page_count": 25,
            "attachment_number": 1,
            "description": "Test document",
            "date_created": "2023-01-01T12:00:00",
            "date_modified": "2023-01-02T12:00:00",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/recap-documents/1/",
            "absolute_url": "https://www.courtlistener.com/recap-document/1/"
        }
        doc = RecapDocument(data)
        assert doc.id == 1
        assert doc.docket == "123"
        assert doc.docket_entry == "456"
        assert doc.court == "scotus"
        assert doc.file_url == "https://example.com/doc.pdf"
        assert doc.file_size == 1024000
        assert doc.file_type == "pdf"
        assert doc.is_available is True
        assert doc.page_count == 25
        assert doc.attachment_number == 1
        assert doc.description == "Test document"
        assert doc.date_created == "2023-01-01T12:00:00"
        assert doc.date_modified == "2023-01-02T12:00:00"
        assert doc.resource_uri == "https://api.courtlistener.com/api/rest/v4/recap-documents/1/"
        assert doc.absolute_url == "https://www.courtlistener.com/recap-document/1/"

    def test_init_with_missing_fields(self):
        """Test initialization with missing fields."""
        data = {"id": 1}
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

    def test_init_with_empty_data(self):
        """Test initialization with empty data."""
        data = {}
        doc = RecapDocument(data)
        assert doc.id is None
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

    def test_init_with_none_values(self):
        """Test initialization with None values."""
        data = {
            "id": None,
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
        assert doc.id is None
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

    def test_init_with_partial_data(self):
        """Test initialization with partial data."""
        data = {
            "id": 1,
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000,
            "is_available": True
        }
        doc = RecapDocument(data)
        assert doc.id == 1
        assert doc.file_url == "https://example.com/doc.pdf"
        assert doc.file_size == 1024000
        assert doc.is_available is True
        # Other fields should be None
        assert doc.docket is None
        assert doc.docket_entry is None
        assert doc.court is None
        assert doc.file_type is None
        assert doc.page_count is None
        assert doc.attachment_number is None
        assert doc.description is None
        assert doc.date_created is None
        assert doc.date_modified is None
        assert doc.resource_uri is None
        assert doc.absolute_url is None

    def test_inherits_from_base_model(self):
        """Test that RecapDocument inherits from BaseModel."""
        data = {"id": 1, "file_url": "https://example.com/doc.pdf"}
        doc = RecapDocument(data)
        assert hasattr(doc, 'to_dict')
        assert hasattr(doc, 'to_json')
        assert hasattr(doc, 'get')
        assert hasattr(doc, '__getitem__')
        assert hasattr(doc, '__contains__')
        assert hasattr(doc, '__repr__')
        assert hasattr(doc, '__str__')

    def test_to_dict_includes_all_fields(self):
        """Test that to_dict includes all fields."""
        data = {
            "id": 1,
            "docket": "123",
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000,
            "is_available": True
        }
        doc = RecapDocument(data)
        result = doc.to_dict()
        assert result["id"] == 1
        assert result["docket"] == "123"
        assert result["file_url"] == "https://example.com/doc.pdf"
        assert result["file_size"] == 1024000
        assert result["is_available"] is True

    def test_to_dict_with_none_values(self):
        """Test to_dict with None values."""
        data = {"id": 1}
        doc = RecapDocument(data)
        result = doc.to_dict()
        assert result["id"] == 1
        assert result["docket"] is None
        assert result["file_url"] is None
        assert result["file_size"] is None
        assert result["is_available"] is None

    def test_repr_with_id(self):
        """Test __repr__ with id."""
        data = {"id": 1, "file_url": "https://example.com/doc.pdf"}
        doc = RecapDocument(data)
        # Should use BaseModel's __repr__ which shows id
        assert "RecapDocument(id=1)" in repr(doc)

    def test_repr_without_id(self):
        """Test __repr__ without id."""
        data = {"file_url": "https://example.com/doc.pdf"}
        doc = RecapDocument(data)
        # Should use BaseModel's __repr__ fallback
        assert "RecapDocument()" in repr(doc)

    def test_str_uses_repr(self):
        """Test that __str__ uses __repr__."""
        data = {"id": 1, "file_url": "https://example.com/doc.pdf"}
        doc = RecapDocument(data)
        assert str(doc) == repr(doc)

    def test_get_method_works(self):
        """Test that get method works for all fields."""
        data = {
            "id": 1,
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000
        }
        doc = RecapDocument(data)
        assert doc.get("id") == 1
        assert doc.get("file_url") == "https://example.com/doc.pdf"
        assert doc.get("file_size") == 1024000
        assert doc.get("docket") is None
        assert doc.get("missing", "default") == "default"

    def test_getitem_works(self):
        """Test that __getitem__ works for all fields."""
        data = {
            "id": 1,
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000
        }
        doc = RecapDocument(data)
        assert doc["id"] == 1
        assert doc["file_url"] == "https://example.com/doc.pdf"
        assert doc["file_size"] == 1024000

    def test_contains_works(self):
        """Test that __contains__ works for all fields."""
        data = {
            "id": 1,
            "file_url": "https://example.com/doc.pdf",
            "file_size": 1024000
        }
        doc = RecapDocument(data)
        assert "id" in doc
        assert "file_url" in doc
        assert "file_size" in doc
        assert "docket" not in doc
        assert "missing" not in doc

    def test_boolean_fields(self):
        """Test boolean fields work correctly."""
        data = {
            "id": 1,
            "is_available": True
        }
        doc = RecapDocument(data)
        assert doc.is_available is True

        data_false = {
            "id": 1,
            "is_available": False
        }
        doc_false = RecapDocument(data_false)
        assert doc_false.is_available is False

    def test_numeric_fields(self):
        """Test numeric fields work correctly."""
        data = {
            "id": 1,
            "file_size": 1024000,
            "page_count": 25,
            "attachment_number": 1
        }
        doc = RecapDocument(data)
        assert doc.file_size == 1024000
        assert doc.page_count == 25
        assert doc.attachment_number == 1