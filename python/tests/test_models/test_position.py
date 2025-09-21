import pytest
from courtlistener.models.position import Position
from datetime import datetime, timedelta

def test_from_dict_and_to_dict():
    now = datetime.now()
    data = {
        'id': 100,
        'judge': 1,
        'court': 2,
        'position_type': 'jud',
        'title': 'District Judge',
        'date_start': now.isoformat(),
        'date_termination': (now + timedelta(days=365)).isoformat(),
        'vote_yes': 80,
        'vote_no': 20,
        'vote_total': 100,
        'vote_type': 'Senate',
    }
    pos = Position.from_dict(data)
    assert pos.id == 100
    assert pos.judge == 1
    assert pos.court == 2
    assert pos.position_type == 'jud'
    assert pos.title == 'District Judge'
    assert isinstance(pos.date_start, datetime)
    assert isinstance(pos.date_termination, datetime)
    assert pos.is_active is False
    assert pos.has_vote_data is True
    assert pos.vote_percentage == 80.0
    summary = pos.get_vote_summary()
    assert summary['yes'] == 80
    assert summary['no'] == 20
    assert summary['total'] == 100
    assert summary['percentage_yes'] == 80.0
    d = pos.to_dict()
    assert d['id'] == 100
    assert d['judge'] == 1
    assert d['court'] == 2
    assert d['position_type'] == 'jud'
    assert d['title'] == 'District Judge'

def test_edge_cases():
    # Missing optional fields
    pos = Position.from_dict({'id': 101})
    assert pos.id == 101
    assert pos.is_active is True
    assert pos.has_vote_data is False
    assert pos.vote_percentage is None
    # Invalid date
    pos = Position.from_dict({'id': 102, 'date_start': 'not-a-date'})
    assert pos.date_start is None 