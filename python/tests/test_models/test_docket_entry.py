import pytest
from courtlistener.models.docket_entry import DocketEntry
from datetime import datetime

def test_from_dict_and_to_dict():
    data = {
        'id': 1,
        'docket': 42,
        'entry_number': 5,
        'description': 'Order granting motion',
        'date_filed': '2023-01-01T00:00:00Z',
        'recap_documents': ['doc1', 'doc2'],
        'seal': False,
        'recap_documents_count': 2,
        'description_short': 'Order',
    }
    entry = DocketEntry.from_dict(data)
    assert entry.id == 1
    assert entry.docket == 42
    assert entry.entry_number == 5
    assert entry.description == 'Order granting motion'
    assert isinstance(entry.date_filed, datetime)
    assert entry.recap_documents == ['doc1', 'doc2']
    assert entry.has_documents is True
    assert entry.is_sealed is False
    d = entry.to_dict()
    assert d['id'] == 1
    assert d['docket'] == 42
    assert d['entry_number'] == 5
    assert d['description'] == 'Order granting motion'
    assert d['recap_documents'] == ['doc1', 'doc2']
    assert d['recap_documents_count'] == 2
    assert d['description_short'] == 'Order'

def test_edge_cases():
    # Missing optional fields
    entry = DocketEntry.from_dict({'id': 2})
    assert entry.id == 2
    assert entry.docket is None
    assert entry.has_documents is False
    assert entry.is_sealed is False
    # Invalid date
    entry = DocketEntry.from_dict({'id': 3, 'date_filed': 'not-a-date'})
    assert entry.date_filed is None 