"""
Tests for standard API methods (list, get, search) across all API classes.

These tests ensure that the standardized method names work correctly
and maintain backward compatibility with existing method names.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient
from courtlistener.api.dockets import DocketsAPI
from courtlistener.api.opinions import OpinionsAPI
from courtlistener.api.courts import CourtsAPI
from courtlistener.api.judges import JudgesAPI
from courtlistener.api.documents import DocumentsAPI
from courtlistener.api.positions import PositionsAPI
from courtlistener.api.parties import PartiesAPI
from courtlistener.api.clusters import ClustersAPI
from courtlistener.api.citations import CitationsAPI
from courtlistener.api.audio import AudioAPI
from courtlistener.api.attorneys import AttorneysAPI
from courtlistener.api.docket_entries import DocketEntriesAPI
from courtlistener.api.financial import FinancialAPI


class TestStandardMethods:
    """Test standard list(), get(), search() methods across APIs."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
    
    def test_dockets_standard_methods(self):
        """Test standard methods for DocketsAPI."""
        api = DocketsAPI(self.client)
        
        # Mock the underlying methods
        with patch.object(api, 'list_dockets', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1)
        
        with patch.object(api, 'get_docket', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api.client.search, 'search_dockets', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once()
    
    def test_opinions_standard_methods(self):
        """Test standard methods for OpinionsAPI."""
        api = OpinionsAPI(self.client)
        
        with patch.object(api, 'list_opinions', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, filters=None, **{})
        
        with patch.object(api, 'get_opinion', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_opinions', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_courts_standard_methods(self):
        """Test standard methods for CourtsAPI."""
        api = CourtsAPI(self.client)
        
        with patch.object(api, 'list_courts', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, filters=None, **{})
        
        with patch.object(api, 'get_court', return_value=Mock()) as mock_get:
            result = api.get("scotus")
            assert result is not None
            mock_get.assert_called_once_with("scotus")
        
        with patch.object(api, 'search_courts', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_judges_standard_methods(self):
        """Test standard methods for JudgesAPI."""
        api = JudgesAPI(self.client)
        
        with patch.object(api, 'list_judges', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1)
        
        with patch.object(api, 'get_judge', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_judges', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_documents_standard_methods(self):
        """Test standard methods for DocumentsAPI."""
        api = DocumentsAPI(self.client)
        
        with patch.object(api, 'list_documents', return_value={}) as mock_list:
            result = api.list(page=1)
            assert result == {}
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_document', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_documents', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_positions_standard_methods(self):
        """Test standard methods for PositionsAPI."""
        api = PositionsAPI(self.client)
        
        with patch.object(api, 'list_positions', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_position', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_positions', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_parties_standard_methods(self):
        """Test standard methods for PartiesAPI."""
        api = PartiesAPI(self.client)
        
        with patch.object(api, 'list_parties', return_value={}) as mock_list:
            result = api.list(page=1)
            assert result == {}
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_party', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_parties', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_clusters_standard_methods(self):
        """Test standard methods for ClustersAPI."""
        api = ClustersAPI(self.client)
        
        with patch.object(api, 'list_clusters', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_cluster', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_clusters', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_citations_standard_methods(self):
        """Test standard methods for CitationsAPI."""
        api = CitationsAPI(self.client)
        
        with patch.object(api, 'list_citations', return_value={}) as mock_list:
            result = api.list(page=1)
            assert result == {}
            mock_list.assert_called_once_with(page=1, **{})
        
        with patch.object(api.client, 'get', return_value={}) as mock_get:
            result = api.get(123)
            assert result == {}
            mock_get.assert_called_once_with('citations/123/')
        
        with patch.object(api, 'search_citations', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once_with(page=1, **{'q': 'test query'})
    
    def test_audio_standard_methods(self):
        """Test standard methods for AudioAPI."""
        api = AudioAPI(self.client)
        
        with patch.object(api, 'list_audio', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_audio', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_audio', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_attorneys_standard_methods(self):
        """Test standard methods for AttorneysAPI."""
        api = AttorneysAPI(self.client)
        
        with patch.object(api, 'list_attorneys', return_value={}) as mock_list:
            result = api.list(page=1)
            assert result == {}
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_attorney', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_attorneys', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_docket_entries_standard_methods(self):
        """Test standard methods for DocketEntriesAPI."""
        api = DocketEntriesAPI(self.client)
        
        with patch.object(api, 'list_entries', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once()
        
        with patch.object(api, 'get_entry', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_docket_entries', return_value={}) as mock_search:
            result = api.search("test query")
            assert result == {}
            mock_search.assert_called_once_with(page=1, **{})
    
    def test_financial_standard_methods(self):
        """Test standard methods for FinancialAPI."""
        api = FinancialAPI(self.client)
        
        with patch.object(api, 'list_financial_disclosures', return_value=[]) as mock_list:
            result = api.list(page=1)
            assert result == []
            mock_list.assert_called_once_with(page=1, q=None, **{})
        
        with patch.object(api, 'get_disclosure', return_value=Mock()) as mock_get:
            result = api.get(123)
            assert result is not None
            mock_get.assert_called_once_with(123)
        
        with patch.object(api, 'search_financial_disclosures', return_value=[]) as mock_search:
            result = api.search("test query")
            assert result == []
            mock_search.assert_called_once_with(q="test query", page=1)
    
    def test_backward_compatibility(self):
        """Test that old method names still work."""
        api = DocketsAPI(self.client)
        
        # Old methods should still exist
        assert hasattr(api, 'list_dockets')
        assert hasattr(api, 'get_docket')
        assert hasattr(api, 'search_dockets')
        
        # New methods should also exist
        assert hasattr(api, 'list')
        assert hasattr(api, 'get')
        assert hasattr(api, 'search')


