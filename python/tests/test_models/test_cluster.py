import pytest
from courtlistener.models.cluster import OpinionCluster
from datetime import datetime

def test_from_dict_and_to_dict():
    data = {
        'id': 10,
        'case_name': 'Roe v. Wade',
        'date_filed': '1973-01-22T00:00:00Z',
        'citations': [{'cite': '410 U.S. 113'}],
        'sub_opinions': [{'type': '010combined'}, {'type': '020concurring'}],
        'panel': [{'name': 'Justice A'}, {'name': 'Justice B'}],
        'precedential': True,
        'blocked': False,
        'citation_count': 1,
        'scdb_id': 'SCDB123',
    }
    cluster = OpinionCluster.from_dict(data)
    assert cluster.id == 10
    assert cluster.case_name == 'Roe v. Wade'
    assert hasattr(cluster, 'date_filed')
    assert cluster.has_citations is True
    assert cluster.is_precedential is True
    assert cluster.is_blocked is False
    assert cluster.has_scdb_data is True
    assert cluster.get_majority_opinion()['type'] == '010combined'
    assert len(cluster.get_concurring_opinions()) == 1
    assert cluster.get_judge_names() == ['Justice A', 'Justice B']
    d = cluster.to_dict()
    assert d['id'] == 10
    assert d['case_name'] == 'Roe v. Wade'
    assert d['precedential'] is True
    assert d['blocked'] is False

def test_edge_cases():
    # Missing optional fields
    cluster = OpinionCluster.from_dict({'id': 11})
    assert cluster.id == 11
    assert cluster.has_citations is False
    assert cluster.is_precedential is True
    assert cluster.is_blocked is False
    assert cluster.has_scdb_data is False
    # Invalid date
    cluster = OpinionCluster.from_dict({'id': 12, 'date_filed': 'not-a-date'})
    assert cluster.date_filed is None 