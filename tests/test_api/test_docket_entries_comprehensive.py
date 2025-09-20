"""
Comprehensive tests for Docket Entries API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.docket_entries import DocketEntriesAPI
from courtlistener.models.docket_entry import DocketEntry
from courtlistener.exceptions import NotFoundError, CourtListenerError


class TestDocketEntriesAPIComprehensive:
    """Comprehensive tests for DocketEntriesAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = DocketEntriesAPI(self.mock_client)
    
    def test_init(self):
        """Test DocketEntriesAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "/api/rest/v4/docket-entries/"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "docket-entries/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == DocketEntry
    
    def test_list_entries_basic(self):
        """Test basic list_entries functionality."""
        mock_response = {
            "results": [
                {"id": 1, "entry_number": 1, "description": "Test Entry 1"},
                {"id": 2, "entry_number": 2, "description": "Test Entry 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_entries()
        
        assert len(result) == 2
        assert all(isinstance(e, DocketEntry) for e in result)
        self.mock_client.get.assert_called_once_with("docket-entries/", params={})
    
    def test_list_entries_with_docket_id(self):
        """Test list_entries with docket ID."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_entries(docket_id=1)
        
        expected_params = {"docket": 1}
        self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
    
    def test_list_entries_with_filters(self):
        """Test list_entries with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.docket_entries.build_filters') as mock_build_filters:
            mock_build_filters.return_value = {"date_filed": "2023-01-01"}
            
            filters = {"date_filed": "2023-01-01"}
            self.api.list_entries(filters=filters)
            
            mock_build_filters.assert_called_once_with(date_filed="2023-01-01")
            expected_params = {"date_filed": "2023-01-01"}
            self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
    
    def test_list_entries_with_limit(self):
        """Test list_entries with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_entries(limit=10)
        
        expected_params = {"limit": 10}
        self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
    
    def test_list_entries_with_all_parameters(self):
        """Test list_entries with all parameters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.docket_entries.build_filters') as mock_build_filters:
            mock_build_filters.return_value = {"date_filed": "2023-01-01"}
            
            filters = {"date_filed": "2023-01-01"}
            self.api.list_entries(docket_id=1, filters=filters, limit=10)
            
            expected_params = {"docket": 1, "date_filed": "2023-01-01", "limit": 10}
            self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
    
    def test_list_entries_empty_results(self):
        """Test list_entries with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_entries()
        
        assert result == []
    
    def test_list_entries_no_results_key(self):
        """Test list_entries when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_entries()
        
        assert result == []
    
    def test_get_entry_success(self):
        """Test get_entry with valid entry ID."""
        mock_response = {"id": 1, "entry_number": 1, "description": "Test Entry"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_entry(1)
        
        assert isinstance(result, DocketEntry)
        self.mock_client.get.assert_called_once_with("docket-entries/1/")
    
    def test_get_entry_not_found(self):
        """Test get_entry with non-existent entry ID."""
        self.mock_client.get.side_effect = NotFoundError("Entry not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_entry(999)
    
    def test_get_entries_by_date_range_basic(self):
        """Test get_entries_by_date_range without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_by_date_range(1, "2023-01-01", "2023-12-31")
            
            expected_filters = {
                'docket': 1,
                'date_filed__gte': '2023-01-01',
                'date_filed__lte': '2023-12-31'
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []
    
    def test_get_entries_by_date_range_with_limit(self):
        """Test get_entries_by_date_range with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_by_date_range(1, "2023-01-01", "2023-12-31", limit=10)
            
            expected_filters = {
                'docket': 1,
                'date_filed__gte': '2023-01-01',
                'date_filed__lte': '2023-12-31'
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []
    
    def test_get_entries_by_number(self):
        """Test get_entries_by_number method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_by_number(1, 5)
            
            expected_filters = {
                'docket': 1,
                'entry_number': 5
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters)
            assert result == []
    
    def test_get_entries_by_description_basic(self):
        """Test get_entries_by_description without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_by_description(1, "motion")
            
            expected_filters = {
                'docket': 1,
                'description__icontains': 'motion'
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []
    
    def test_get_entries_by_description_with_limit(self):
        """Test get_entries_by_description with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_by_description(1, "motion", limit=10)
            
            expected_filters = {
                'docket': 1,
                'description__icontains': 'motion'
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []
    
    def test_get_entries_with_documents_basic(self):
        """Test get_entries_with_documents without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_with_documents(1)
            
            expected_filters = {
                'docket': 1,
                'recap_documents__isnull': False
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []
    
    def test_get_entries_with_documents_with_limit(self):
        """Test get_entries_with_documents with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_entries') as mock_list_entries:
            mock_list_entries.return_value = []
            
            result = self.api.get_entries_with_documents(1, limit=10)
            
            expected_filters = {
                'docket': 1,
                'recap_documents__isnull': False
            }
            mock_list_entries.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []
    
    def test_list_docket_entries_basic(self):
        """Test list_docket_entries without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_docket_entries()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("docket-entries/", params={"page": 1})
    
    def test_list_docket_entries_with_filters(self):
        """Test list_docket_entries with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"docket": 1, "date_filed": "2023-01-01"}
        result = self.api.list_docket_entries(page=2, **filters)
        
        expected_params = {"docket": 1, "date_filed": "2023-01-01", "page": 2}
        self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
        assert result == mock_response
    
    def test_search_docket_entries_basic(self):
        """Test search_docket_entries without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_docket_entries()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("docket-entries/", params={"page": 1})
    
    def test_search_docket_entries_with_filters(self):
        """Test search_docket_entries with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"docket": 1, "description": "motion"}
        result = self.api.search_docket_entries(page=2, **filters)
        
        expected_params = {"docket": 1, "description": "motion", "page": 2}
        self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
        assert result == mock_response
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_entries()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_entry(1)
