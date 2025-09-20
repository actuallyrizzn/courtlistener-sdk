"""
Final comprehensive tests for Search API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from courtlistener.api.search import SearchAPI, SearchResult
from courtlistener.exceptions import CourtListenerError


class TestSearchAPIComprehensiveFinal:
    """Final comprehensive tests for SearchAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = SearchAPI(self.mock_client)
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "search/"
    
    def test_search_result_parse_data_opinion(self):
        """Test SearchResult._parse_data with opinion resource_uri."""
        result = SearchResult({"resource_uri": "/api/rest/v4/opinions/123/"})
        result._parse_data()
        
        assert result.result_type == 'opinion'
    
    def test_search_result_parse_data_docket(self):
        """Test SearchResult._parse_data with docket resource_uri."""
        result = SearchResult({"resource_uri": "/api/rest/v4/dockets/456/"})
        result._parse_data()
        
        assert result.result_type == 'docket'
    
    def test_search_result_parse_data_judge(self):
        """Test SearchResult._parse_data with judge resource_uri."""
        result = SearchResult({"resource_uri": "/api/rest/v4/judges/789/"})
        result._parse_data()
        
        assert result.result_type == 'judge'
    
    def test_search_result_parse_data_audio(self):
        """Test SearchResult._parse_data with audio resource_uri."""
        result = SearchResult({"resource_uri": "/api/rest/v4/audio/101/"})
        result._parse_data()
        
        assert result.result_type == 'audio'
    
    def test_search_result_parse_data_unknown(self):
        """Test SearchResult._parse_data with unknown resource_uri."""
        result = SearchResult({"resource_uri": "/api/rest/v4/unknown/999/"})
        result._parse_data()
        
        assert result.result_type == 'unknown'
    
    def test_search_result_parse_data_no_resource_uri(self):
        """Test SearchResult._parse_data without resource_uri."""
        result = SearchResult({"id": 123, "name": "test"})
        result._parse_data()
        
        # Should not have result_type attribute
        assert not hasattr(result, 'result_type')
    
    def test_search_judges_with_filters(self):
        """Test search_judges with filters parameter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus"}
        result = self.api.search_judges("test query", filters)
        
        expected_params = {"q": "test query", "page": 1, "type": "j", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_judges_no_filters(self):
        """Test search_judges without filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_judges("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "j"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_judges_none_filters(self):
        """Test search_judges with None filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_judges("test query", filters=None)
        
        expected_params = {"q": "test query", "page": 1, "type": "j"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_all_with_result_type_and_filters(self):
        """Test search_all with both result_type and filters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([
            {"resource_uri": "/api/rest/v4/opinions/123/"},
            {"resource_uri": "/api/rest/v4/opinions/456/"}
        ]))
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test", result_type="o", filters={"court": "scotus"}))
            
            expected_params = {"q": "test", "type": "o", "court": "scotus"}
            mock_paginator_class.assert_called_once_with(self.mock_client, "search/", expected_params)
            assert len(result) == 2
            assert all(isinstance(r, SearchResult) for r in result)
    
    def test_search_all_no_result_type_no_filters(self):
        """Test search_all with no result_type and no filters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test"))
            
            expected_params = {"q": "test"}
            mock_paginator_class.assert_called_once_with(self.mock_client, "search/", expected_params)
            assert result == []
    
    def test_search_all_with_result_type_no_filters(self):
        """Test search_all with result_type but no filters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test", result_type="d"))
            
            expected_params = {"q": "test", "type": "d"}
            mock_paginator_class.assert_called_once_with(self.mock_client, "search/", expected_params)
            assert result == []
    
    def test_search_all_no_result_type_with_filters(self):
        """Test search_all with no result_type but with filters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        
        with patch('courtlistener.api.search.PageIterator') as mock_paginator_class:
            mock_paginator_class.return_value = mock_paginator
            
            result = list(self.api.search_all("test", filters={"court": "scotus"}))
            
            expected_params = {"q": "test", "court": "scotus"}
            mock_paginator_class.assert_called_once_with(self.mock_client, "search/", expected_params)
            assert result == []
    
    def test_search_opinions_all_with_filters(self):
        """Test search_opinions_all with filters."""
        mock_paginator = Mock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_opinions_all("test", {"court": "scotus"}))
            
            mock_search_all.assert_called_once_with("test", result_type='o', filters={"court": "scotus"})
            assert result == []
    
    def test_search_opinions_all_no_filters(self):
        """Test search_opinions_all without filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_opinions_all("test"))
            
            mock_search_all.assert_called_once_with("test", result_type='o', filters=None)
            assert result == []
    
    def test_search_dockets_all_with_filters(self):
        """Test search_dockets_all with filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_dockets_all("test", {"court": "scotus"}))
            
            mock_search_all.assert_called_once_with("test", result_type='d', filters={"court": "scotus"})
            assert result == []
    
    def test_search_dockets_all_no_filters(self):
        """Test search_dockets_all without filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_dockets_all("test"))
            
            mock_search_all.assert_called_once_with("test", result_type='d', filters=None)
            assert result == []
    
    def test_search_judges_all_with_filters(self):
        """Test search_judges_all with filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_judges_all("test", {"court": "scotus"}))
            
            mock_search_all.assert_called_once_with("test", result_type='j', filters={"court": "scotus"})
            assert result == []
    
    def test_search_judges_all_no_filters(self):
        """Test search_judges_all without filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_judges_all("test"))
            
            mock_search_all.assert_called_once_with("test", result_type='j', filters=None)
            assert result == []
    
    def test_search_audio_all_with_filters(self):
        """Test search_audio_all with filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_audio_all("test", {"court": "scotus"}))
            
            mock_search_all.assert_called_once_with("test", result_type='oa', filters={"court": "scotus"})
            assert result == []
    
    def test_search_audio_all_no_filters(self):
        """Test search_audio_all without filters."""
        with patch.object(self.api, 'search_all') as mock_search_all:
            mock_search_all.return_value = iter([])
            
            result = list(self.api.search_audio_all("test"))
            
            mock_search_all.assert_called_once_with("test", result_type='oa', filters=None)
            assert result == []
    
    def test_list_search_with_query(self):
        """Test list_search with query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search(page=2, q="test query")
        
        expected_params = {"q": "test query", "page": 2}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_list_search_no_query(self):
        """Test list_search without query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search(page=2)
        
        expected_params = {"q": "", "page": 2}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_list_search_with_filters(self):
        """Test list_search with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_search(page=1, q="test", court="scotus")
        
        expected_params = {"q": "test", "page": 1, "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_documents_basic(self):
        """Test search_documents basic functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_documents("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "documents"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_documents_with_filters(self):
        """Test search_documents with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_documents("test query", page=2, court="scotus")
        
        expected_params = {"q": "test query", "page": 2, "type": "documents", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_people_basic(self):
        """Test search_people basic functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_people("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "people"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_people_with_filters(self):
        """Test search_people with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_people("test query", page=2, court="scotus")
        
        expected_params = {"q": "test query", "page": 2, "type": "people", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_recap_basic(self):
        """Test search_recap basic functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_recap("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "recap"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_recap_with_filters(self):
        """Test search_recap with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_recap("test query", page=2, court="scotus")
        
        expected_params = {"q": "test query", "page": 2, "type": "recap", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_oral_arguments_basic(self):
        """Test search_oral_arguments basic functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_oral_arguments("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "oral_arguments"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_oral_arguments_with_filters(self):
        """Test search_oral_arguments with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_oral_arguments("test query", page=2, court="scotus")
        
        expected_params = {"q": "test query", "page": 2, "type": "oral_arguments", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_opinions_clusters_basic(self):
        """Test search_opinions_clusters basic functionality."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinions_clusters("test query")
        
        expected_params = {"q": "test query", "page": 1, "type": "clusters"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_search_opinions_clusters_with_filters(self):
        """Test search_opinions_clusters with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinions_clusters("test query", page=2, court="scotus")
        
        expected_params = {"q": "test query", "page": 2, "type": "clusters", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("search/", params=expected_params)
        assert result == mock_response
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.search("test query")
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.search("test query")
