"""
Comprehensive tests for Search API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.search import SearchAPI, SearchResult
from courtlistener.exceptions import CourtListenerError


class TestSearchResultComprehensive:
    """Comprehensive tests for SearchResult model."""
    
    def test_search_result_parse_data_opinion(self):
        """Test SearchResult parsing with opinion resource URI."""
        data = {"id": 1, "resource_uri": "/api/rest/v4/opinions/123/"}
        result = SearchResult(data)
        
        assert result.result_type == 'opinion'
    
    def test_search_result_parse_data_docket(self):
        """Test SearchResult parsing with docket resource URI."""
        data = {"id": 1, "resource_uri": "/api/rest/v4/dockets/123/"}
        result = SearchResult(data)
        
        assert result.result_type == 'docket'
    
    def test_search_result_parse_data_judge(self):
        """Test SearchResult parsing with judge resource URI."""
        data = {"id": 1, "resource_uri": "/api/rest/v4/judges/123/"}
        result = SearchResult(data)
        
        assert result.result_type == 'judge'
    
    def test_search_result_parse_data_audio(self):
        """Test SearchResult parsing with audio resource URI."""
        data = {"id": 1, "resource_uri": "/api/rest/v4/audio/123/"}
        result = SearchResult(data)
        
        assert result.result_type == 'audio'
    
    def test_search_result_parse_data_unknown(self):
        """Test SearchResult parsing with unknown resource URI."""
        data = {"id": 1, "resource_uri": "/api/rest/v4/unknown/123/"}
        result = SearchResult(data)
        
        assert result.result_type == 'unknown'
    
    def test_search_result_parse_data_no_resource_uri(self):
        """Test SearchResult parsing without resource_uri."""
        data = {"id": 1}
        result = SearchResult(data)
        
        # Should not have result_type attribute if no resource_uri
        assert not hasattr(result, 'result_type')


class TestSearchAPIComprehensive:
    """Comprehensive tests for SearchAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SearchAPI(self.mock_client)
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "search/"
    
    def test_search_basic(self):
        """Test basic search functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search("test query")
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("search/", params={"q": "test query", "page": 1})
    
    def test_search_with_page(self):
        """Test search with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.search("test query", page=2)
        
        self.mock_client.get.assert_called_once_with("search/", params={"q": "test query", "page": 2})
    
    def test_search_with_filters(self):
        """Test search with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus", "date_filed": "2023-01-01"}
        self.api.search("test query", page=1, **filters)
        
        expected_params = {"q": "test query", "page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_opinions(self):
        """Test search_opinions method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinions("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "opinions", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_dockets(self):
        """Test search_dockets method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_dockets("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "dockets", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_clusters(self):
        """Test search_clusters method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_clusters("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "clusters", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_judges_basic(self):
        """Test search_judges method without filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_judges("test query")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 1, "result_type": "j"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_judges_with_filters(self):
        """Test search_judges method with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus"}
        result = self.api.search_judges("test query", filters=filters)
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 1, "result_type": "j", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_audio(self):
        """Test search_audio method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_audio("test query", page=2, duration_min=60)
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "audio", "duration_min": 60}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_all_basic(self):
        """Test search_all method without filters or result_type."""
        mock_search_data = [
            {"id": 1, "resource_uri": "/api/rest/v4/opinions/123/"},
            {"id": 2, "resource_uri": "/api/rest/v4/dockets/456/"}
        ]
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter(mock_search_data))
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test query"))
            
            assert len(result) == 2
            assert all(isinstance(r, SearchResult) for r in result)
            mock_paginator_class.assert_called_once_with(self.mock_client, 'search/', {'q': 'test query'})
    
    def test_search_all_with_result_type(self):
        """Test search_all method with result_type."""
        mock_search_data = [{"id": 1, "resource_uri": "/api/rest/v4/opinions/123/"}]
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter(mock_search_data))
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test query", result_type="o"))
            
            assert len(result) == 1
            mock_paginator_class.assert_called_once_with(self.mock_client, 'search/', {'q': 'test query', 'type': 'o'})
    
    def test_search_all_with_filters(self):
        """Test search_all method with filters."""
        mock_search_data = []
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter(mock_search_data))
            mock_paginator_class.return_value = mock_paginator
            
            filters = {"court": "scotus"}
            result = list(self.api.search_all("test query", filters=filters))
            
            assert result == []
            expected_params = {'q': 'test query', 'court': 'scotus'}
            mock_paginator_class.assert_called_once_with(self.mock_client, 'search/', expected_params)
    
    def test_search_all_with_result_type_and_filters(self):
        """Test search_all method with both result_type and filters."""
        mock_search_data = []
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator.__iter__ = Mock(return_value=iter(mock_search_data))
            mock_paginator_class.return_value = mock_paginator
            
            filters = {"court": "scotus"}
            result = list(self.api.search_all("test query", result_type="o", filters=filters))
            
            assert result == []
            expected_params = {'q': 'test query', 'type': 'o', 'court': 'scotus'}
            mock_paginator_class.assert_called_once_with(self.mock_client, 'search/', expected_params)
    
    def test_search_opinions_all(self):
        """Test search_opinions_all method."""
        mock_search_data = [{"id": 1, "resource_uri": "/api/rest/v4/opinions/123/"}]
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            result = list(self.api.search_opinions_all("test query"))
            
            assert len(result) == 1
            mock_search_all.assert_called_once_with("test query", result_type='o', filters=None)
    
    def test_search_opinions_all_with_filters(self):
        """Test search_opinions_all method with filters."""
        mock_search_data = []
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            filters = {"court": "scotus"}
            result = list(self.api.search_opinions_all("test query", filters))
            
            assert result == []
            mock_search_all.assert_called_once_with("test query", result_type='o', filters=filters)
    
    def test_search_dockets_all(self):
        """Test search_dockets_all method."""
        mock_search_data = [{"id": 1, "resource_uri": "/api/rest/v4/dockets/123/"}]
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            result = list(self.api.search_dockets_all("test query"))
            
            assert len(result) == 1
            mock_search_all.assert_called_once_with("test query", result_type='d', filters=None)
    
    def test_search_dockets_all_with_filters(self):
        """Test search_dockets_all method with filters."""
        mock_search_data = []
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            filters = {"court": "scotus"}
            result = list(self.api.search_dockets_all("test query", filters))
            
            assert result == []
            mock_search_all.assert_called_once_with("test query", result_type='d', filters=filters)
    
    def test_search_judges_all(self):
        """Test search_judges_all method."""
        mock_search_data = [{"id": 1, "resource_uri": "/api/rest/v4/judges/123/"}]
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            result = list(self.api.search_judges_all("test query"))
            
            assert len(result) == 1
            mock_search_all.assert_called_once_with("test query", result_type='j', filters=None)
    
    def test_search_judges_all_with_filters(self):
        """Test search_judges_all method with filters."""
        mock_search_data = []
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            filters = {"court": "scotus"}
            result = list(self.api.search_judges_all("test query", filters))
            
            assert result == []
            mock_search_all.assert_called_once_with("test query", result_type='j', filters=filters)
    
    def test_search_audio_all(self):
        """Test search_audio_all method."""
        mock_search_data = [{"id": 1, "resource_uri": "/api/rest/v4/audio/123/"}]
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            result = list(self.api.search_audio_all("test query"))
            
            assert len(result) == 1
            mock_search_all.assert_called_once_with("test query", result_type='oa', filters=None)
    
    def test_search_audio_all_with_filters(self):
        """Test search_audio_all method with filters."""
        mock_search_data = []
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter(mock_search_data)
            
            filters = {"court": "scotus"}
            result = list(self.api.search_audio_all("test query", filters))
            
            assert result == []
            mock_search_all.assert_called_once_with("test query", result_type='oa', filters=filters)
    
    def test_list_search_basic(self):
        """Test list_search method without query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("search/", params={"q": "", "page": 1})
    
    def test_list_search_with_query(self):
        """Test list_search method with query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search(q="test query", page=2)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("search/", params={"q": "test query", "page": 2})
    
    def test_list_search_with_filters(self):
        """Test list_search method with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search(q="test query", page=1, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 1, "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_documents(self):
        """Test search_documents method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_documents("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "documents", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_people(self):
        """Test search_people method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_people("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "people", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_recap(self):
        """Test search_recap method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_recap("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "recap", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_oral_arguments(self):
        """Test search_oral_arguments method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_oral_arguments("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "oral_arguments", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_search_opinions_clusters(self):
        """Test search_opinions_clusters method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinions_clusters("test query", page=2, court="scotus")
        
        assert result == mock_response
        expected_params = {"q": "test query", "page": 2, "type": "clusters", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.search("test query")
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.search_opinions("test query")
