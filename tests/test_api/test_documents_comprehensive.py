"""
Comprehensive tests for Documents API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.documents import DocumentsAPI, Document
from courtlistener.exceptions import ValidationError, CourtListenerError


class TestDocumentsAPIComprehensive:
    """Comprehensive tests for DocumentsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = DocumentsAPI(self.mock_client)
    
    def test_init(self):
        """Test DocumentsAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "documents/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Document
    
    def test_list_documents_basic(self):
        """Test basic list_documents functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_documents()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("documents/", params={"page": 1})
    
    def test_list_documents_with_page(self):
        """Test list_documents with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_documents(page=2)
        
        self.mock_client.get.assert_called_once_with("documents/", params={"page": 2})
    
    def test_list_documents_with_query(self):
        """Test list_documents with search query."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_documents(q="motion")
        
        self.mock_client.get.assert_called_once_with("documents/", params={"page": 1, "q": "motion"})
    
    def test_list_documents_with_filters(self):
        """Test list_documents with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"docket": 1, "document_type": "motion"}
        self.api.list_documents(page=1, **filters)
        
        expected_params = {"page": 1, "docket": 1, "document_type": "motion"}
        self.mock_client.get.assert_called_once_with("documents/", params=expected_params)
    
    def test_list_documents_with_query_and_filters(self):
        """Test list_documents with both query and filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"docket": 1}
        self.api.list_documents(q="motion", page=2, **filters)
        
        expected_params = {"page": 2, "q": "motion", "docket": 1}
        self.mock_client.get.assert_called_once_with("documents/", params=expected_params)
    
    def test_list_documents_no_filters(self):
        """Test list_documents with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_documents(page=1)
        
        self.mock_client.get.assert_called_once_with("documents/", params={"page": 1})
    
    def test_get_document_success(self):
        """Test get_document with valid document ID."""
        mock_response = {"id": 1, "name": "Test Document", "document_type": "motion"}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.documents.validate_id') as mock_validate:
            result = self.api.get_document(1)
            
            assert isinstance(result, Document)
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("recap-documents/1/")
    
    def test_get_document_invalid_id(self):
        """Test get_document with invalid document ID."""
        with patch('courtlistener.api.documents.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_document(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_document_not_found(self):
        """Test get_document with non-existent document ID."""
        with patch('courtlistener.api.documents.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("Document not found")
            
            with pytest.raises(CourtListenerError):
                self.api.get_document(999)
    
    def test_search_documents_basic(self):
        """Test search_documents without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_documents("motion")
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("documents/", params={"q": "motion", "page": 1})
    
    def test_search_documents_with_page(self):
        """Test search_documents with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_documents("motion", page=2)
        
        self.mock_client.get.assert_called_once_with("documents/", params={"q": "motion", "page": 2})
    
    def test_search_documents_with_filters(self):
        """Test search_documents with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"docket": 1, "document_type": "motion"}
        self.api.search_documents("motion", page=1, **filters)
        
        expected_params = {"q": "motion", "page": 1, "docket": 1, "document_type": "motion"}
        self.mock_client.get.assert_called_once_with("documents/", params=expected_params)
    
    def test_search_documents_no_filters(self):
        """Test search_documents with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_documents("motion", page=1)
        
        self.mock_client.get.assert_called_once_with("documents/", params={"q": "motion", "page": 1})
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_documents()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.search_documents("motion")
