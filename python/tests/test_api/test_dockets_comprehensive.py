"""
Comprehensive tests for Dockets API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from courtlistener.api.dockets import DocketsAPI
from courtlistener.models.docket import Docket
from courtlistener.exceptions import NotFoundError, ValidationError


class TestDocketsAPIComprehensive:
    """Comprehensive tests for DocketsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client.config.base_url = "https://api.courtlistener.com/api/rest/v4"
        self.api = DocketsAPI(self.mock_client)
    
    def test_init(self):
        """Test DocketsAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "https://api.courtlistener.com/api/rest/v4/dockets"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "dockets/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Docket
    
    def test_list_dockets_basic(self):
        """Test basic list_dockets functionality."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Case 1"},
                {"id": 2, "case_name": "Test Case 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_dockets()
        
        assert len(result) == 2
        assert all(isinstance(d, Docket) for d in result)
        self.mock_client.get.assert_called_once_with("dockets/", params={"page": 1})
    
    def test_list_dockets_with_page(self):
        """Test list_dockets with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_dockets(page=2)
        
        self.mock_client.get.assert_called_once_with("dockets/", params={"page": 2})
    
    def test_list_dockets_with_filters(self):
        """Test list_dockets with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus", "date_filed": "2023-01-01"}
        self.api.list_dockets(page=1, **filters)
        
        expected_params = {"page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("dockets/", params=expected_params)
    
    def test_list_dockets_empty_results(self):
        """Test list_dockets with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_dockets()
        
        assert result == []
    
    def test_list_dockets_no_results_key(self):
        """Test list_dockets when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_dockets()
        
        assert result == []
    
    def test_get_docket_success(self):
        """Test get_docket with valid docket ID."""
        mock_response = {"id": 1, "case_name": "Test Case"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_docket(1)
        
        assert isinstance(result, Docket)
        self.mock_client.get.assert_called_once_with("dockets/1/")
    
    def test_get_docket_not_found(self):
        """Test get_docket with non-existent docket ID."""
        self.mock_client.get.side_effect = NotFoundError("Docket not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_docket(999)
    
    def test_get_docket_by_number_success(self):
        """Test get_docket_by_number with valid docket number."""
        mock_response = {"results": [{"id": 1, "docket_number": "1:23-cv-12345"}]}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_dockets') as mock_list_dockets:
            mock_list_dockets.return_value = [Docket({"id": 1, "docket_number": "1:23-cv-12345"})]
            
            result = self.api.get_docket_by_number("1:23-cv-12345")
            
            assert isinstance(result, Docket)
            mock_list_dockets.assert_called_once_with({"docket_number": "1:23-cv-12345"})
    
    def test_get_docket_by_number_with_court(self):
        """Test get_docket_by_number with court filter."""
        mock_response = {"results": [{"id": 1, "docket_number": "1:23-cv-12345"}]}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_dockets') as mock_list_dockets:
            mock_list_dockets.return_value = [Docket({"id": 1, "docket_number": "1:23-cv-12345"})]
            
            result = self.api.get_docket_by_number("1:23-cv-12345", court="scotus")
            
            assert isinstance(result, Docket)
            mock_list_dockets.assert_called_once_with({"docket_number": "1:23-cv-12345", "court": "scotus"})
    
    def test_get_docket_by_number_not_found(self):
        """Test get_docket_by_number when docket not found."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_docket_by_number("nonexistent")
        
        assert result is None
    
    def test_get_docket_by_number_invalid_docket_number(self):
        """Test get_docket_by_number with invalid docket number."""
        with pytest.raises(ValidationError):
            self.api.get_docket_by_number("")
    
    def test_get_dockets_by_court_basic(self):
        """Test get_dockets_by_court without additional filters."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_dockets') as mock_list_dockets:
            mock_list_dockets.return_value = [Docket({"id": 1, "case_name": "Test Case"})]
            
            result = self.api.get_dockets_by_court("scotus")
            
            assert len(result) == 1
            mock_list_dockets.assert_called_once_with({"court": "scotus"})
    
    def test_get_dockets_by_court_with_filters(self):
        """Test get_dockets_by_court with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(self.api, 'list_dockets') as mock_list_dockets:
            mock_list_dockets.return_value = []
            
            filters = {"date_filed": "2023-01-01"}
            result = self.api.get_dockets_by_court("scotus", filters)
            
            assert result == []
            mock_list_dockets.assert_called_once_with({"court": "scotus", "date_filed": "2023-01-01"})
    
    def test_get_docket_entries(self):
        """Test get_docket_entries method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_docket_entries(1, page=2, status="filed")
        
        expected_params = {"docket": 1, "page": 2, "status": "filed"}
        self.mock_client.get.assert_called_once_with("docket-entries/", params=expected_params)
        assert result == mock_response
    
    def test_get_documents(self):
        """Test get_documents method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_documents(1, page=2, document_type="motion")
        
        expected_params = {"docket": 1, "page": 2, "document_type": "motion"}
        self.mock_client.get.assert_called_once_with("documents/", params=expected_params)
        assert result == mock_response
    
    def test_get_parties(self):
        """Test get_parties method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_parties(1, page=2, party_type="defendant")
        
        expected_params = {"docket": 1, "page": 2, "party_type": "defendant"}
        self.mock_client.get.assert_called_once_with("parties/", params=expected_params)
        assert result == mock_response
    
    def test_get_audio(self):
        """Test get_audio method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_audio(1, page=2, duration_min=60)
        
        expected_params = {"docket": 1, "page": 2, "duration_min": 60}
        self.mock_client.get.assert_called_once_with("audio/", params=expected_params)
        assert result == mock_response
    
    def test_get_financial(self):
        """Test get_financial method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_financial(1, page=2, year=2023)
        
        expected_params = {"docket": 1, "page": 2, "year": 2023}
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params=expected_params)
        assert result == mock_response
    
    def test_get_dockets_by_date_range_basic(self):
        """Test get_dockets_by_date_range with start and end dates."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.dockets.build_date_range_filter') as mock_build_filter:
            mock_build_filter.return_value = {"date_filed__gte": "2023-01-01", "date_filed__lte": "2023-12-31"}
            
            result = self.api.get_dockets_by_date_range("2023-01-01", "2023-12-31")
            
            mock_build_filter.assert_called_once_with("date_filed", "2023-01-01", "2023-12-31")
            self.mock_client.get.assert_called_once()
    
    def test_get_dockets_by_date_range_with_court(self):
        """Test get_dockets_by_date_range with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.dockets.build_date_range_filter') as mock_build_filter:
            with patch('courtlistener.api.dockets.combine_filters') as mock_combine:
                mock_build_filter.return_value = {"date_filed__gte": "2023-01-01"}
                mock_combine.return_value = {"date_filed__gte": "2023-01-01", "court": "scotus"}
                
                result = self.api.get_dockets_by_date_range("2023-01-01", court="scotus")
                
                mock_combine.assert_called_once()
                self.mock_client.get.assert_called_once()
    
    def test_get_dockets_by_date_range_with_additional_filters(self):
        """Test get_dockets_by_date_range with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.dockets.build_date_range_filter') as mock_build_filter:
            with patch('courtlistener.api.dockets.combine_filters') as mock_combine:
                mock_build_filter.return_value = {"date_filed__gte": "2023-01-01"}
                mock_combine.return_value = {"date_filed__gte": "2023-01-01", "status": "filed"}
                
                additional_filters = {"status": "filed"}
                result = self.api.get_dockets_by_date_range("2023-01-01", filters=additional_filters)
                
                mock_combine.assert_called_once()
                self.mock_client.get.assert_called_once()
    
    def test_get_dockets_by_date_range_no_dates(self):
        """Test get_dockets_by_date_range with no dates."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.dockets.build_date_range_filter') as mock_build_filter:
            with patch('courtlistener.api.dockets.combine_filters') as mock_combine:
                mock_build_filter.return_value = {}
                mock_combine.return_value = {}
                
                result = self.api.get_dockets_by_date_range()
                
                mock_combine.assert_called_once()
                self.mock_client.get.assert_called_once()
    
    def test_list_all_dockets(self):
        """Test list_all_dockets iterator."""
        mock_docket_data = [{"id": 1, "case_name": "Test Case 1"}, {"id": 2, "case_name": "Test Case 2"}]
        
        with patch('courtlistener.api.dockets.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter(mock_docket_data))
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.list_all_dockets())
            
            assert len(result) == 2
            assert all(isinstance(d, Docket) for d in result)
            mock_paginator_class.assert_called_once_with(self.mock_client, self.api.base_url, None)
    
    def test_list_all_dockets_with_filters(self):
        """Test list_all_dockets with filters."""
        filters = {"court": "scotus"}
        
        with patch('courtlistener.api.dockets.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter([]))
            mock_paginator_class.return_value = mock_paginator
            
            list(self.api.list_all_dockets(filters))
            
            mock_paginator_class.assert_called_once_with(self.mock_client, self.api.base_url, filters)
    
    def test_get_dockets_by_court_all(self):
        """Test get_dockets_by_court_all iterator."""
        mock_docket_data = [{"id": 1, "case_name": "Test Case"}]
        
        with patch.object(self.api, 'list_all_dockets') as mock_list_all:
            mock_list_all.return_value = iter(mock_docket_data)
            
            result = list(self.api.get_dockets_by_court_all("scotus"))
            
            assert len(result) == 1
            mock_list_all.assert_called_once_with({"court": "scotus"})
    
    def test_get_dockets_by_court_all_with_filters(self):
        """Test get_dockets_by_court_all with additional filters."""
        filters = {"date_filed": "2023-01-01"}
        
        with patch.object(self.api, 'list_all_dockets') as mock_list_all:
            mock_list_all.return_value = iter([])
            
            list(self.api.get_dockets_by_court_all("scotus", filters))
            
            expected_filters = {"court": "scotus", "date_filed": "2023-01-01"}
            mock_list_all.assert_called_once_with(expected_filters)
    
    def test_search_dockets(self):
        """Test search_dockets method."""
        mock_search_result = {"results": []}
        self.mock_client.search.search_dockets.return_value = mock_search_result
        
        result = self.api.search_dockets("test query", {"court": "scotus"})
        
        self.mock_client.search.search_dockets.assert_called_once_with("test query", {"court": "scotus"})
        assert result == mock_search_result
    
    def test_search_dockets_no_filters(self):
        """Test search_dockets without filters."""
        mock_search_result = {"results": []}
        self.mock_client.search.search_dockets.return_value = mock_search_result
        
        result = self.api.search_dockets("test query")
        
        self.mock_client.search.search_dockets.assert_called_once_with("test query", None)
        assert result == mock_search_result
    
    def test_search_dockets_all(self):
        """Test search_dockets_all iterator."""
        mock_search_results = [
            Mock(resource_uri="/api/rest/v4/dockets/123/"),
            Mock(resource_uri="/api/rest/v4/opinions/456/"),
            Mock(resource_uri="/api/rest/v4/dockets/789/")
        ]
        self.mock_client.search.search_dockets_all.return_value = mock_search_results
        
        with patch.object(self.api, 'get_docket') as mock_get_docket:
            mock_get_docket.side_effect = [Docket({"id": 123}), Docket({"id": 789})]
            
            result = list(self.api.search_dockets_all("test query"))
            
            assert len(result) == 2
            assert all(isinstance(d, Docket) for d in result)
            mock_get_docket.assert_any_call(123)
            mock_get_docket.assert_any_call(789)
    
    def test_search_dockets_all_with_filters(self):
        """Test search_dockets_all with filters."""
        mock_search_results = []
        self.mock_client.search.search_dockets_all.return_value = mock_search_results
        
        result = list(self.api.search_dockets_all("test query", {"court": "scotus"}))
        
        self.mock_client.search.search_dockets_all.assert_called_once_with("test query", {"court": "scotus"})
        assert result == []
    
    def test_search_dockets_all_no_docket_results(self):
        """Test search_dockets_all with no docket results."""
        mock_search_results = [
            Mock(resource_uri="/api/rest/v4/opinions/456/"),
            Mock(resource_uri="/api/rest/v4/courts/789/")
        ]
        self.mock_client.search.search_dockets_all.return_value = mock_search_results
        
        result = list(self.api.search_dockets_all("test query"))
        
        assert result == []
    
    def test_search_dockets_all_invalid_resource_uri(self):
        """Test search_dockets_all with invalid resource URI."""
        mock_search_results = [
            Mock(resource_uri="invalid-uri")
        ]
        self.mock_client.search.search_dockets_all.return_value = mock_search_results
        
        result = list(self.api.search_dockets_all("test query"))
        
        assert result == []
    
    def test_search_dockets_all_no_resource_uri(self):
        """Test search_dockets_all with result that has no resource_uri."""
        mock_search_results = [
            Mock(spec=[])  # Mock without resource_uri attribute
        ]
        self.mock_client.search.search_dockets_all.return_value = mock_search_results
        
        result = list(self.api.search_dockets_all("test query"))
        
        assert result == []
