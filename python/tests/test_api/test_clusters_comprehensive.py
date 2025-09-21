"""
Comprehensive tests for the Clusters API module.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.clusters import ClustersAPI
from courtlistener.models.cluster import OpinionCluster


class TestClustersAPI:
    """Test cases for ClustersAPI."""

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

    def test_list_clusters(self):
        """Test list_clusters method."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Case 1"},
                {"id": 2, "case_name": "Test Case 2"}
            ]
        }
        self.mock_client.get.return_value = mock_response

        result = self.api.list_clusters()

        expected_params = {"page": 1}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
        assert len(result) == 2
        assert all(isinstance(item, OpinionCluster) for item in result)

    def test_list_clusters_with_query(self):
        """Test list_clusters method with query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list_clusters(page=2, q="test query")

        expected_params = {"page": 2, "q": "test query"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
        assert result == []

    def test_list_clusters_with_filters(self):
        """Test list_clusters method with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list_clusters(court=1, date_filed="2023-01-01")

        expected_params = {"page": 1, "court": 1, "date_filed": "2023-01-01"}
        self.mock_client.get.assert_called_once_with("/clusters/", params=expected_params)
        assert result == []

    def test_get_cluster(self):
        """Test get_cluster method."""
        mock_response = {"id": 1, "case_name": "Test Case"}
        self.mock_client.get.return_value = mock_response

        result = self.api.get_cluster(1)

        self.mock_client.get.assert_called_once_with("/clusters/1/")
        assert isinstance(result, OpinionCluster)

    def test_get_clusters_by_court(self):
        """Test get_clusters_by_court method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_court(1)

            expected_filters = {'court': 1}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_by_court_with_filters(self):
        """Test get_clusters_by_court method with additional filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_court(1, filters={'date_filed': '2023-01-01'}, limit=10)

            expected_filters = {'court': 1, 'date_filed': '2023-01-01'}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []

    def test_get_cluster_by_citation(self):
        """Test get_cluster_by_citation method."""
        mock_response = {"results": [{"id": 1, "case_name": "Test Case"}]}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = [OpinionCluster({"id": 1, "case_name": "Test Case"})]

            result = self.api.get_cluster_by_citation("410 U.S. 113")

            expected_filters = {'citations__cite': "410 U.S. 113"}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=1)
            assert isinstance(result, OpinionCluster)

    def test_get_cluster_by_citation_not_found(self):
        """Test get_cluster_by_citation method when no cluster found."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_cluster_by_citation("410 U.S. 113")

            expected_filters = {'citations__cite': "410 U.S. 113"}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=1)
            assert result is None

    def test_get_clusters_by_case_name(self):
        """Test get_clusters_by_case_name method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_case_name("Test Case")

            expected_filters = {'case_name__icontains': "Test Case"}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_by_case_name_with_court(self):
        """Test get_clusters_by_case_name method with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_case_name("Test Case", court_id=1, limit=5)

            expected_filters = {'case_name__icontains': "Test Case", 'court': 1}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=5)
            assert result == []

    def test_get_clusters_by_date_range(self):
        """Test get_clusters_by_date_range method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_date_range("2023-01-01", "2023-12-31")

            expected_filters = {
                'date_filed__gte': "2023-01-01",
                'date_filed__lte': "2023-12-31"
            }
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_by_date_range_with_court(self):
        """Test get_clusters_by_date_range method with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_date_range("2023-01-01", "2023-12-31", court_id=1, limit=10)

            expected_filters = {
                'date_filed__gte': "2023-01-01",
                'date_filed__lte': "2023-12-31",
                'court': 1
            }
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []

    def test_get_clusters_by_docket(self):
        """Test get_clusters_by_docket method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_docket(1)

            expected_filters = {'docket': 1}
            mock_list_clusters.assert_called_once_with(filters=expected_filters)
            assert result == []

    def test_get_clusters_by_judge(self):
        """Test get_clusters_by_judge method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_judge(1)

            expected_filters = {'sub_opinions__author': 1}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_by_judge_with_limit(self):
        """Test get_clusters_by_judge method with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_judge(1, limit=5)

            expected_filters = {'sub_opinions__author': 1}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=5)
            assert result == []

    def test_get_clusters_by_jurisdiction(self):
        """Test get_clusters_by_jurisdiction method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_jurisdiction("F")

            expected_filters = {'court__jurisdiction': "F"}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_by_jurisdiction_with_limit(self):
        """Test get_clusters_by_jurisdiction method with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_by_jurisdiction("S", limit=10)

            expected_filters = {'court__jurisdiction': "S"}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=10)
            assert result == []

    def test_get_clusters_with_citations(self):
        """Test get_clusters_with_citations method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_with_citations()

            expected_filters = {'citations__isnull': False}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=None)
            assert result == []

    def test_get_clusters_with_citations_with_limit(self):
        """Test get_clusters_with_citations method with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.get_clusters_with_citations(limit=5)

            expected_filters = {'citations__isnull': False}
            mock_list_clusters.assert_called_once_with(filters=expected_filters, limit=5)
            assert result == []

    def test_list_opinion_clusters(self):
        """Test list_opinion_clusters method."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list_opinion_clusters()

        expected_params = {"page": 1}
        self.mock_client.get.assert_called_once_with('clusters/', params=expected_params)
        assert result == mock_response

    def test_list_opinion_clusters_with_filters(self):
        """Test list_opinion_clusters method with filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list_opinion_clusters(page=2, court=1)

        expected_params = {"page": 2, "court": 1}
        self.mock_client.get.assert_called_once_with('clusters/', params=expected_params)
        assert result == mock_response

    def test_search_opinion_clusters(self):
        """Test search_opinion_clusters method."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.search_opinion_clusters()

        expected_params = {"page": 1}
        self.mock_client.get.assert_called_once_with('clusters/', params=expected_params)
        assert result == mock_response

    def test_search_opinion_clusters_with_query(self):
        """Test search_opinion_clusters method with query."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.search_opinion_clusters(q="test query", page=2)

        expected_params = {"page": 2, "q": "test query"}
        self.mock_client.get.assert_called_once_with('clusters/', params=expected_params)
        assert result == mock_response

    def test_search_opinion_clusters_with_filters(self):
        """Test search_opinion_clusters method with filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.search_opinion_clusters(q="test", court=1, page=1)

        expected_params = {"page": 1, "q": "test", "court": 1}
        self.mock_client.get.assert_called_once_with('clusters/', params=expected_params)
        assert result == mock_response

    def test_search_clusters(self):
        """Test search_clusters method."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.search_clusters("test query")

            mock_list_clusters.assert_called_once_with(page=1, q="test query")
            assert result == []

    def test_search_clusters_with_filters(self):
        """Test search_clusters method with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response

        with patch.object(self.api, 'list_clusters') as mock_list_clusters:
            mock_list_clusters.return_value = []

            result = self.api.search_clusters("test query", page=2, court=1)

            mock_list_clusters.assert_called_once_with(page=2, q="test query", court=1)
            assert result == []