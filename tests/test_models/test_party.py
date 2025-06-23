import pytest
from courtlistener.models.party import Party
from datetime import datetime


class TestParty:
    def test_from_dict_and_to_dict(self):
        """Test Party model serialization and deserialization."""
        data = {
            'id': 1,
            'name': 'John Smith',
            'type': 'defendant',
            'docket': 1,
            'attorney': 1,
            'date_terminated': '2021-01-01T00:00:00Z',
            'absolute_url': '/party/1/',
            'resource_uri': '/api/rest/v4/parties/1/'
        }
        
        party = Party.from_dict(data)
        assert party.id == 1
        assert party.name == 'John Smith'
        assert party.type == 'defendant'
        assert party.docket == 1
        assert party.attorney == 1
        assert isinstance(party.date_terminated, datetime)
        assert party.absolute_url == '/party/1/'
        assert party.resource_uri == '/api/rest/v4/parties/1/'
        
        # Test to_dict
        d = party.to_dict()
        assert d['id'] == 1
        assert d['name'] == 'John Smith'
        assert d['type'] == 'defendant'
        assert d['docket'] == 1
    
    def test_edge_cases(self):
        """Test Party model edge cases."""
        # Missing optional fields
        party = Party.from_dict({'id': 2})
        assert party.id == 2
        assert party.name is None
        assert party.type is None
        assert party.docket is None
        assert party.attorney is None
        assert party.date_terminated is None
        
        # Invalid dates
        party = Party.from_dict({'id': 3, 'date_terminated': 'not-a-date'})
        assert party.date_terminated is None
    
    def test_properties(self):
        """Test Party model properties."""
        party = Party.from_dict({
            'id': 4,
            'date_terminated': '2021-01-01T00:00:00Z'
        })
        assert party.is_terminated is True
        
        party = Party.from_dict({'id': 5})
        assert party.is_terminated is False
        
        party = Party.from_dict({
            'id': 6,
            'type': 'plaintiff'
        })
        assert party.is_plaintiff is True
        
        party = Party.from_dict({
            'id': 7,
            'type': 'defendant'
        })
        assert party.is_defendant is True
        
        party = Party.from_dict({
            'id': 8,
            'type': 'intervenor'
        })
        assert party.is_intervenor is True
        
        party = Party.from_dict({
            'id': 9,
            'type': 'unknown'
        })
        assert party.is_plaintiff is False
        assert party.is_defendant is False
        assert party.is_intervenor is False
    
    def test_string_representations(self):
        """Test Party model string representations."""
        party = Party.from_dict({
            'id': 10,
            'name': 'John Smith',
            'type': 'defendant'
        })
        
        assert str(party) == "Party(id=10, name='John Smith', type='defendant')"
        assert repr(party) == "<Party(id=10, name='John Smith', type='defendant', docket=None)>" 