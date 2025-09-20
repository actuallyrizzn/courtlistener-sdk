"""
Comprehensive tests for Opinions API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.opinions import OpinionsAPI
from courtlistener.models.opinion import Opinion
from courtlistener.exceptions import NotFoundError, CourtListenerError


class TestOpinionsAPIComprehensive:
    """Comprehensive tests for OpinionsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client.config.base_url = "https://api.courtlistener.com/api/rest/v4"
        self.api = OpinionsAPI(self.mock_client)
    
    def test_init(self):
        """Test OpinionsAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "https://api.courtlistener.com/api/rest/v4/opinions"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "opinions/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Opinion
    
    def test_list_opinions_basic(self):
        """Test basic list_opinions functionality."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Case 1"},
                {"id": 2, "case_name": "Test Case 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinions()
        
        assert len(result) == 2
        assert all(isinstance(o, Opinion) for o in result)
        self.mock_client.get.assert_called_once_with("/opinions/", params={"page": 1})
    
    def test_list_opinions_with_page(self):
        """Test list_opinions with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_opinions(page=2)
        
        self.mock_client.get.assert_called_once_with("/opinions/", params={"page": 2})
    
    def test_list_opinions_with_query(self):
        """Test list_opinions with search query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_opinions(q="constitutional")
        
        self.mock_client.get.assert_called_once_with("/opinions/", params={"page": 1, "q": "constitutional"})
    
    def test_list_opinions_with_filters(self):
        """Test list_opinions with filters parameter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus", "date_filed": "2023-01-01"}
        self.api.list_opinions(page=1, filters=filters)
        
        expected_params = {"page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_list_opinions_with_kwargs(self):
        """Test list_opinions with additional kwargs."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_opinions(page=1, court="scotus", date_filed="2023-01-01")
        
        expected_params = {"page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_list_opinions_with_filters_and_kwargs(self):
        """Test list_opinions with both filters and kwargs."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus"}
        self.api.list_opinions(page=1, filters=filters, date_filed="2023-01-01")
        
        expected_params = {"page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_list_opinions_empty_results(self):
        """Test list_opinions with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinions()
        
        assert result == []
    
    def test_list_opinions_no_results_key(self):
        """Test list_opinions when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinions()
        
        assert result == []
    
    def test_get_opinion_success(self):
        """Test get_opinion with valid opinion ID."""
        mock_response = {"id": 1, "case_name": "Test Case"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinion(1)
        
        assert isinstance(result, Opinion)
        self.mock_client.get.assert_called_once_with("/opinions/1/")
    
    def test_get_opinion_not_found(self):
        """Test get_opinion with non-existent opinion ID."""
        self.mock_client.get.side_effect = NotFoundError("Opinion not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_opinion(999)
    
    def test_search_opinions(self):
        """Test search_opinions method."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_opinions("constitutional", page=2, court="scotus")
        
        assert len(result) == 1
        expected_params = {"page": 2, "q": "constitutional", "court": "scotus"}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_get_opinion_cluster(self):
        """Test get_opinion_cluster method."""
        mock_response = {"id": 1, "case_name": "Test Cluster"}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinion_cluster(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("/clusters/1/")
    
    def test_list_opinion_clusters_basic(self):
        """Test list_opinion_clusters without filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_opinion_clusters()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("/clusters/", params={"page": 1})
    
    def test_list_opinion_clusters_with_filters(self):
        """Test list_opinion_clusters with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": "scotus", "date_filed": "2023-01-01"}
        result = self.api.list_opinion_clusters(page=2, **filters)
        
        expected_params = {"page": 2, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
        assert result == mock_response
    
    def test_get_opinions_in_cluster_basic(self):
        """Test get_opinions_in_cluster without additional filters."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Opinion 1"},
                {"id": 2, "case_name": "Test Opinion 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinions_in_cluster(1)
        
        assert len(result) == 2
        assert all(isinstance(o, Opinion) for o in result)
        expected_params = {"cluster": 1}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_get_opinions_in_cluster_with_filters(self):
        """Test get_opinions_in_cluster with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinions_in_cluster(1, court="scotus", date_filed="2023-01-01")
        
        assert result == []
        expected_params = {"cluster": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_get_opinions_in_cluster_empty_results(self):
        """Test get_opinions_in_cluster with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinions_in_cluster(1)
        
        assert result == []
    
    def test_get_opinions_in_cluster_no_results_key(self):
        """Test get_opinions_in_cluster when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_opinions_in_cluster(1)
        
        assert result == []
    
    def test_get_citations_basic(self):
        """Test get_citations without additional filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_citations(1)
        
        assert result == mock_response
        expected_params = {"citing_opinion": 1}
        self.mock_client.get.assert_called_once_with("/opinions-cited/", params=expected_params)
    
    def test_get_citations_with_filters(self):
        """Test get_citations with additional filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_citations(1, page=2, limit=10)
        
        assert result == mock_response
        expected_params = {"citing_opinion": 1, "page": 2, "limit": 10}
        self.mock_client.get.assert_called_once_with("/opinions-cited/", params=expected_params)
    
    def test_get_sub_opinions_basic(self):
        """Test get_sub_opinions without additional filters."""
        mock_response = {
            "results": [
                {"id": 2, "case_name": "Concurring Opinion"},
                {"id": 3, "case_name": "Dissenting Opinion"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_sub_opinions(1)
        
        assert len(result) == 2
        assert all(isinstance(o, Opinion) for o in result)
        expected_params = {"parent_opinion": 1}
        self.mock_client.get.assert_called_once_with("/opinions/", params=expected_params)
    
    def test_get_sub_opinions_empty_results(self):
        """Test get_sub_opinions with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_sub_opinions(1)
        
        assert result == []
    
    def test_get_sub_opinions_no_results_key(self):
        """Test get_sub_opinions when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_sub_opinions(1)
        
        assert result == []
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_opinions()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_opinion(1)
