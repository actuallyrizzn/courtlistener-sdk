import pytest
from unittest.mock import MagicMock
from courtlistener.api.clusters import ClustersAPI
from courtlistener.models.cluster import OpinionCluster

def make_api():
    mock_client = MagicMock()
    api = ClustersAPI(mock_client)
    return api, mock_client

def test_list_clusters():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 1}]}
    results = api.list_clusters()
    assert isinstance(results[0], OpinionCluster)
    assert results[0].id == 1
    mock_client.get.assert_called_once()

def test_get_cluster():
    api, mock_client = make_api()
    mock_client.get.return_value = {'id': 2}
    cluster = api.get_cluster(2)
    assert isinstance(cluster, OpinionCluster)
    assert cluster.id == 2
    mock_client.get.assert_called_once()

def test_get_clusters_by_court():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 3}]}
    results = api.get_clusters_by_court(5)
    assert results[0].id == 3
    mock_client.get.assert_called_once()

def test_get_cluster_by_citation():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 4}]}
    cluster = api.get_cluster_by_citation('410 U.S. 113')
    assert cluster.id == 4
    mock_client.get.assert_called_once()

def test_get_clusters_by_case_name():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 5}]}
    results = api.get_clusters_by_case_name('Roe')
    assert results[0].id == 5
    mock_client.get.assert_called_once()

def test_get_clusters_by_date_range():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 6}]}
    results = api.get_clusters_by_date_range('2020-01-01', '2020-12-31')
    assert results[0].id == 6
    mock_client.get.assert_called_once()

def test_get_clusters_by_docket():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 7}]}
    results = api.get_clusters_by_docket(9)
    assert results[0].id == 7
    mock_client.get.assert_called_once()

def test_get_clusters_by_judge():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 8}]}
    results = api.get_clusters_by_judge(11)
    assert results[0].id == 8
    mock_client.get.assert_called_once()

def test_get_clusters_by_jurisdiction():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 9}]}
    results = api.get_clusters_by_jurisdiction('F')
    assert results[0].id == 9
    mock_client.get.assert_called_once()

def test_get_clusters_with_citations():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 10}]}
    results = api.get_clusters_with_citations()
    assert results[0].id == 10
    mock_client.get.assert_called_once() 