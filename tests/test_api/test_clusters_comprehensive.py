"""
Comprehensive tests for Clusters API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.clusters import ClustersAPI
from courtlistener.models.cluster import OpinionCluster
from courtlistener.exceptions import NotFoundError, CourtListenerError


class TestClustersAPIComprehensive:
    """Comprehensive tests for ClustersAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = ClustersAPI(self.mock_client)
    
    def test_init(self):
        """Test ClustersAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "/api/rest/v4/clusters/"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "clusters/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == OpinionCluster
    
    def test_list_clusters_basic(self):
        """Test basic list_clusters functionality."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Case 1"},
                {"id": 2, "case_name": "Test Case 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_clusters()
        
        assert len(result) == 2
        assert all(isinstance(c, OpinionCluster) for c in result)
        self.mock_client.get.assert_called_once_with("/clusters/", params={"page": 1})
    
    def test_list_clusters_with_page(self):
        """Test list_clusters with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_clusters(page=2)
        
        self.mock_client.get.assert_called_once_with("/clusters/", params={"page": 2})
    
    def test_list_clusters_with_query(self):
        """Test list_clusters with search query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_clusters(q="test query")
        
        self.mock_client.get.assert_called_once_with("/clusters/", params={"page": 1, "q": "test query"})
    
    def test_list_clusters_with_filters(self):
        """Test list_clusters with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": 1, "date_filed": "2023-01-01"}
        self.api.list_clusters(page=1, **filters)
        
        expected_params = {"page": 1, "court": 1, "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_list_clusters_empty_results(self):
        """Test list_clusters with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_clusters()
        
        assert result == []
    
    def test_list_clusters_no_results_key(self):
        """Test list_clusters when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_clusters()
        
        assert result == []
    
    def test_get_cluster_success(self):
        """Test get_cluster with valid cluster ID."""
        mock_response = {"id": 1, "case_name": "Test Case"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_cluster(1)
        
        assert isinstance(result, OpinionCluster)
        self.mock_client.get.assert_called_once_with("/clusters/1/")
    
    def test_get_cluster_not_found(self):
        """Test get_cluster with non-existent cluster ID."""
        self.mock_client.get.side_effect = NotFoundError("Cluster not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_cluster(999)
    
    def test_get_clusters_by_court_basic(self):
        """Test get_clusters_by_court without additional filters."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_clusters_by_court(1)
        
        assert len(result) == 1
        self.mock_client.get.assert_called_once_with("/clusters/", params={"page": 1, "court": 1})
    
    def test_get_clusters_by_court_with_filters(self):
        """Test get_clusters_by_court with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"date_filed": "2023-01-01"}
        self.api.get_clusters_by_court(1, filters)
        
        expected_params = {"page": 1, "court": 1, "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_court_with_limit(self):
        """Test get_clusters_by_court with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_court(1, limit=10)
        
        expected_params = {"page": 1, "court": 1, "limit": 10}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_cluster_by_citation_found(self):
        """Test get_cluster_by_citation when cluster is found."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_cluster_by_citation("410 U.S. 113")
        
        assert isinstance(result, OpinionCluster)
        expected_params = {"page": 1, "citations__cite": "410 U.S. 113"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_cluster_by_citation_not_found(self):
        """Test get_cluster_by_citation when cluster is not found."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_cluster_by_citation("nonexistent citation")
        
        assert result is None
    
    def test_get_clusters_by_case_name_basic(self):
        """Test get_clusters_by_case_name without court filter."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_clusters_by_case_name("Test Case")
        
        assert len(result) == 1
        expected_params = {"page": 1, "case_name__icontains": "Test Case"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_case_name_with_court(self):
        """Test get_clusters_by_case_name with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_case_name("Test Case", court_id=1)
        
        expected_params = {"page": 1, "case_name__icontains": "Test Case", "court": 1}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_case_name_with_limit(self):
        """Test get_clusters_by_case_name with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_case_name("Test Case", limit=10)
        
        expected_params = {"page": 1, "case_name__icontains": "Test Case", "limit": 10}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_date_range_basic(self):
        """Test get_clusters_by_date_range without court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_date_range("2023-01-01", "2023-12-31")
        
        expected_params = {
            "page": 1,
            "date_filed__gte": "2023-01-01",
            "date_filed__lte": "2023-12-31"
        }
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_date_range_with_court(self):
        """Test get_clusters_by_date_range with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_date_range("2023-01-01", "2023-12-31", court_id=1)
        
        expected_params = {
            "page": 1,
            "date_filed__gte": "2023-01-01",
            "date_filed__lte": "2023-12-31",
            "court": 1
        }
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_date_range_with_limit(self):
        """Test get_clusters_by_date_range with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_date_range("2023-01-01", "2023-12-31", limit=10)
        
        expected_params = {
            "page": 1,
            "date_filed__gte": "2023-01-01",
            "date_filed__lte": "2023-12-31",
            "limit": 10
        }
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_docket(self):
        """Test get_clusters_by_docket method."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_clusters_by_docket(1)
        
        assert len(result) == 1
        expected_params = {"page": 1, "docket": 1}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_judge_basic(self):
        """Test get_clusters_by_judge without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_judge(1)
        
        expected_params = {"page": 1, "sub_opinions__author": 1}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_judge_with_limit(self):
        """Test get_clusters_by_judge with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_judge(1, limit=10)
        
        expected_params = {"page": 1, "sub_opinions__author": 1, "limit": 10}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_jurisdiction_basic(self):
        """Test get_clusters_by_jurisdiction without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_jurisdiction("F")
        
        expected_params = {"page": 1, "court__jurisdiction": "F"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_by_jurisdiction_with_limit(self):
        """Test get_clusters_by_jurisdiction with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_by_jurisdiction("S", limit=10)
        
        expected_params = {"page": 1, "court__jurisdiction": "S", "limit": 10}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_with_citations_basic(self):
        """Test get_clusters_with_citations without limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_with_citations()
        
        expected_params = {"page": 1, "citations__isnull": False}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_get_clusters_with_citations_with_limit(self):
        """Test get_clusters_with_citations with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_clusters_with_citations(limit=10)
        
        expected_params = {"page": 1, "citations__isnull": False, "limit": 10}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_list_opinion_clusters_basic(self):
        """Test list_opinion_clusters without filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinion_clusters()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("clusters/", params={"page": 1})
    
    def test_list_opinion_clusters_with_filters(self):
        """Test list_opinion_clusters with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": 1, "date_filed": "2023-01-01"}
        result = self.api.list_opinion_clusters(page=2, **filters)
        
        expected_params = {"court": 1, "date_filed": "2023-01-01", "page": 2}
        self.mock_client.get.assert_called_once_with("clusters/", params=expected_params)
        assert result == mock_response
    
    def test_list_opinion_clusters_no_filters(self):
        """Test list_opinion_clusters with no filters parameter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinion_clusters(page=1)
        
        self.mock_client.get.assert_called_once_with("clusters/", params={"page": 1})
        assert result == mock_response
    
    def test_search_opinion_clusters_basic(self):
        """Test search_opinion_clusters without query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinion_clusters()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("clusters/", params={"page": 1})
    
    def test_search_opinion_clusters_with_query(self):
        """Test search_opinion_clusters with query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinion_clusters(q="test query")
        
        expected_params = {"page": 1, "q": "test query"}
        self.mock_client.get.assert_called_once_with("clusters/", params=expected_params)
        assert result == mock_response
    
    def test_search_opinion_clusters_with_filters(self):
        """Test search_opinion_clusters with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": 1}
        result = self.api.search_opinion_clusters(q="test", page=2, **filters)
        
        expected_params = {"court": 1, "page": 2, "q": "test"}
        self.mock_client.get.assert_called_once_with("clusters/", params=expected_params)
        assert result == mock_response
    
    def test_search_opinion_clusters_no_filters(self):
        """Test search_opinion_clusters with no filters parameter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinion_clusters(q="test", page=1)
        
        expected_params = {"page": 1, "q": "test"}
        self.mock_client.get.assert_called_once_with("clusters/", params=expected_params)
        assert result == mock_response
    
    def test_search_clusters(self):
        """Test search_clusters method."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_clusters("test query", page=2, court=1)
        
        assert len(result) == 1
        assert isinstance(result[0], OpinionCluster)
        expected_params = {"page": 2, "q": "test query", "court": 1}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_search_clusters_no_filters(self):
        """Test search_clusters without additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_clusters("test query")
        
        assert result == []
        expected_params = {"page": 1, "q": "test query"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_clusters()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_cluster(1)
