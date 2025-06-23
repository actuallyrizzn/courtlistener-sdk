import pytest
from courtlistener.models.document import Document
from datetime import datetime


class TestDocument:
    def test_from_dict_and_to_dict(self):
        """Test Document model serialization and deserialization."""
        data = {
            'id': 1,
            'docket': 1,
            'docket_entry': 1,
            'document_number': '1',
            'document_type': 'motion',
            'description': 'Motion to Dismiss',
            'filepath_local': '/path/to/file.pdf',
            'filepath_ia': 'https://archive.org/file.pdf',
            'filepath_ia_json': 'https://archive.org/file.json',
            'plain_text': 'This is the document text',
            'html': '<p>This is the document text</p>',
            'html_lawbox': '<p>Lawbox version</p>',
            'html_columbia': '<p>Columbia version</p>',
            'html_anon_2020': '<p>Anonymous version</p>',
            'absolute_url': '/document/1/',
            'resource_uri': '/api/rest/v4/documents/1/'
        }
        
        document = Document.from_dict(data)
        assert document.id == 1
        assert document.docket == 1
        assert document.docket_entry == 1
        assert document.document_number == '1'
        assert document.document_type == 'motion'
        assert document.description == 'Motion to Dismiss'
        assert document.filepath_local == '/path/to/file.pdf'
        assert document.filepath_ia == 'https://archive.org/file.pdf'
        assert document.filepath_ia_json == 'https://archive.org/file.json'
        assert document.plain_text == 'This is the document text'
        assert document.html == '<p>This is the document text</p>'
        assert document.html_lawbox == '<p>Lawbox version</p>'
        assert document.html_columbia == '<p>Columbia version</p>'
        assert document.html_anon_2020 == '<p>Anonymous version</p>'
        assert document.absolute_url == '/document/1/'
        assert document.resource_uri == '/api/rest/v4/documents/1/'
        
        # Test to_dict
        d = document.to_dict()
        assert d['id'] == 1
        assert d['docket'] == 1
        assert d['document_number'] == '1'
        assert d['document_type'] == 'motion'
    
    def test_edge_cases(self):
        """Test Document model edge cases."""
        # Missing optional fields
        document = Document.from_dict({'id': 2})
        assert document.id == 2
        assert document.docket is None
        assert document.docket_entry is None
        assert document.document_number is None
        assert document.document_type is None
        assert document.description is None
        assert document.filepath_local is None
        
        # Empty strings
        document = Document.from_dict({
            'id': 3,
            'description': '',
            'plain_text': ''
        })
        assert document.description == ''
        assert document.plain_text == ''
    
    def test_properties(self):
        """Test Document model properties."""
        document = Document.from_dict({
            'id': 4,
            'filepath_local': '/path/to/file.pdf'
        })
        assert document.has_local_file is True
        
        document = Document.from_dict({'id': 5})
        assert document.has_local_file is False
        
        document = Document.from_dict({
            'id': 6,
            'filepath_ia': 'https://archive.org/file.pdf'
        })
        assert document.has_ia_file is True
        
        document = Document.from_dict({'id': 7})
        assert document.has_ia_file is False
        
        document = Document.from_dict({
            'id': 8,
            'document_type': 'motion'
        })
        assert document.is_motion is True
        
        document = Document.from_dict({
            'id': 9,
            'document_type': 'brief'
        })
        assert document.is_brief is True
        
        document = Document.from_dict({
            'id': 10,
            'document_type': 'opinion'
        })
        assert document.is_opinion is True
    
    def test_string_representations(self):
        """Test Document model string representations."""
        document = Document.from_dict({
            'id': 11,
            'document_number': '1',
            'document_type': 'motion',
            'description': 'Motion to Dismiss'
        })
        
        assert str(document) == "Document(id=11, document_number='1', document_type='motion', description='Motion to Dismiss')"
        assert repr(document) == "<Document(id=11, docket=None, document_number='1', document_type='motion')>" 