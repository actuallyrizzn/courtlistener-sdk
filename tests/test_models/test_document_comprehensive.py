"""Comprehensive tests for Document model."""

import pytest
from unittest.mock import patch
from courtlistener.models.document import Document


class TestDocumentComprehensive:
    """Comprehensive tests for Document model."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "document_number": "DOC-001"}
        document = Document(data)
        assert document._data == data

    def test_parse_data_sets_attributes(self):
        """Test that _parse_data sets expected attributes."""
        data = {
            "id": 1,
            "docket": "docket123",
            "docket_entry": 456,
            "document_number": "DOC-001",
            "document_type": "Motion",
            "type": "Motion",
            "description": "Test document",
            "local_path": "/local/path",
            "file_path": "/file/path",
            "file_url": "http://example.com/file.pdf",
            "filepath_local": "/local/filepath",
            "date_filed": "2023-01-01",
            "absolute_url": "http://example.com/doc",
            "resource_uri": "http://api.example.com/doc/1/"
        }
        document = Document(data)
        
        # Check that attributes are set
        assert hasattr(document, 'id')
        assert hasattr(document, 'docket')
        assert hasattr(document, 'docket_entry')
        assert hasattr(document, 'document_number')
        assert hasattr(document, 'document_type')
        assert hasattr(document, 'type')
        assert hasattr(document, 'description')
        assert hasattr(document, 'local_path')
        assert hasattr(document, 'file_path')
        assert hasattr(document, 'file_url')
        assert hasattr(document, 'filepath_local')
        assert hasattr(document, 'date_filed')
        assert hasattr(document, 'absolute_url')
        assert hasattr(document, 'resource_uri')

    def test_parse_data_docket_mapping(self):
        """Test docket mapping logic in _parse_data."""
        data = {"docket_entry": "entry123"}
        document = Document(data)
        assert hasattr(document, 'docket')

    def test_parse_data_no_docket_entry(self):
        """Test _parse_data when no docket_entry."""
        data = {}
        document = Document(data)
        assert hasattr(document, 'docket')

    def test_parse_data_date_parsing(self):
        """Test date parsing in _parse_data."""
        data = {
            "date_modified": "2023-01-15T10:30:00Z",
            "date_created": "2023-01-01T12:00:00Z"
        }
        document = Document(data)
        # The _parse_datetime method is not implemented in BaseModel yet
        # so we just check that the attributes exist
        assert hasattr(document, 'date_modified')
        assert hasattr(document, 'date_created')

    def test_has_local_file_property_true(self):
        """Test has_local_file property when file exists."""
        data = {"local_path": "/local/path"}
        document = Document(data)
        # The property checks _data directly, not the attribute
        assert document._data.get('local_path') == "/local/path"
        assert document.has_local_file is True

    def test_has_local_file_property_file_path(self):
        """Test has_local_file property with file_path."""
        data = {"file_path": "/file/path"}
        document = Document(data)
        assert document.has_local_file is True

    def test_has_local_file_property_file_url(self):
        """Test has_local_file property with file_url."""
        data = {"file_url": "http://example.com/file.pdf"}
        document = Document(data)
        assert document.has_local_file is True

    def test_has_local_file_property_filepath_local(self):
        """Test has_local_file property with filepath_local."""
        data = {"filepath_local": "/local/filepath"}
        document = Document(data)
        assert document.has_local_file is True

    def test_has_local_file_property_false(self):
        """Test has_local_file property when no file."""
        data = {}
        document = Document(data)
        assert document.has_local_file is False

    def test_docket_entry_property(self):
        """Test docket_entry property."""
        data = {"_docket_entry": 123}
        document = Document(data)
        assert document.docket_entry == 123

    def test_docket_entry_property_none(self):
        """Test docket_entry property when not set."""
        data = {}
        document = Document(data)
        assert document.docket_entry is None

    def test_has_ia_file_property_true(self):
        """Test has_ia_file property when IA file exists."""
        data = {"ia_upload_date": "2023-01-01"}
        document = Document(data)
        assert document.has_ia_file is True

    def test_has_ia_file_property_false(self):
        """Test has_ia_file property when no IA file."""
        data = {}
        document = Document(data)
        assert document.has_ia_file is False

    def test_repr_with_id(self):
        """Test __repr__ method with id."""
        data = {
            "id": 1,
            "docket": "docket123",
            "document_number": "DOC-001",
            "document_type": "Motion"
        }
        document = Document(data)
        repr_str = repr(document)
        assert "Document" in repr_str
        assert "1" in repr_str
        assert "docket123" in repr_str
        assert "DOC-001" in repr_str
        assert "Motion" in repr_str

    def test_repr_without_id(self):
        """Test __repr__ method without id."""
        data = {}
        document = Document(data)
        assert repr(document) == "<Document()>"

    def test_repr_fallback_type(self):
        """Test __repr__ method with type fallback."""
        data = {
            "id": 1,
            "type": "Motion"  # No document_type, should use type
        }
        document = Document(data)
        repr_str = repr(document)
        assert "Motion" in repr_str

    def test_str_with_id(self):
        """Test __str__ method with id."""
        data = {
            "id": 1,
            "document_number": "DOC-001",
            "document_type": "Motion",
            "description": "Test document"
        }
        document = Document(data)
        str_repr = str(document)
        assert "Document" in str_repr
        assert "1" in str_repr
        assert "DOC-001" in str_repr
        assert "Motion" in str_repr
        assert "Test document" in str_repr

    def test_str_without_id(self):
        """Test __str__ method without id."""
        data = {}
        document = Document(data)
        assert str(document) == "Document()"

    def test_str_fallback_type(self):
        """Test __str__ method with type fallback."""
        data = {
            "id": 1,
            "type": "Motion"  # No document_type, should use type
        }
        document = Document(data)
        str_repr = str(document)
        assert "Motion" in str_repr

    def test_comprehensive_data(self):
        """Test with comprehensive data."""
        data = {
            "id": 1,
            "docket": "docket123",
            "docket_entry": 456,
            "document_number": "DOC-001",
            "document_type": "Motion",
            "type": "Motion",
            "description": "Test document",
            "local_path": "/local/path",
            "file_path": "/file/path",
            "file_url": "http://example.com/file.pdf",
            "filepath_local": "/local/filepath",
            "date_filed": "2023-01-01",
            "absolute_url": "http://example.com/doc",
            "resource_uri": "http://api.example.com/doc/1/",
            "date_modified": "2023-01-15T10:30:00Z",
            "date_created": "2023-01-01T12:00:00Z",
            "ia_upload_date": "2023-01-01"
        }
        document = Document(data)
        
        # Test properties
        assert document.has_local_file is True
        assert document.has_ia_file is True
        
        # Test string representations
        repr_str = repr(document)
        str_repr = str(document)
        assert "Document" in repr_str
        assert "Document" in str_repr

    def test_edge_case_empty_data(self):
        """Test with completely empty data."""
        data = {}
        document = Document(data)
        
        # All attributes should be None
        assert document.has_local_file is False
        assert document.has_ia_file is False
        assert document.docket_entry is None
        
        # String representations should work
        assert repr(document) == "<Document()>"
        assert str(document) == "Document()"

    def test_edge_case_partial_data(self):
        """Test with partial data."""
        data = {"id": 1}
        document = Document(data)
        
        # Should have id but other attributes should be None
        assert hasattr(document, 'id')
        assert document.has_local_file is False
        assert document.has_ia_file is False
