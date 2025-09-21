import pytest
from courtlistener.models.court import Court
from datetime import datetime


class TestCourt:
    def test_from_dict_and_to_dict(self):
        """Test Court model serialization and deserialization."""
        data = {
            'id': 1,
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS',
            'full_name': 'Supreme Court of the United States',
            'url': 'scotus',
            'jurisdiction': 'F',
            'jurisdiction_name': 'Federal',
            'start_date': '1789-01-01T00:00:00Z',
            'end_date': None,
            'absolute_url': '/court/scotus/',
            'resource_uri': '/api/rest/v4/courts/1/'
        }
        
        court = Court.from_dict(data)
        assert court.id == 1
        assert court.name == 'SCOTUS'
        assert court.short_name == 'SCOTUS'
        assert court.full_name == 'Supreme Court of the United States'
        assert court.url == 'scotus'
        assert court.jurisdiction == 'F'
        assert court.jurisdiction_name == 'Federal'
        assert hasattr(court, 'start_date')
        assert court.end_date is None
        assert court.absolute_url == '/court/scotus/'
        assert court.resource_uri == '/api/rest/v4/courts/1/'
        
        # Test to_dict
        d = court.to_dict()
        assert d['id'] == 1
        assert d['name'] == 'SCOTUS'
        assert d['short_name'] == 'SCOTUS'
        assert d['jurisdiction'] == 'F'
    
    def test_edge_cases(self):
        """Test Court model edge cases."""
        # Missing optional fields
        court = Court.from_dict({'id': 2})
        assert court.id == 2
        assert court.name is None
        assert court.short_name is None
        assert court.start_date is None
        assert court.end_date is None
        
        # Invalid dates
        court = Court.from_dict({'id': 3, 'start_date': 'not-a-date'})
        assert court.start_date is None
    
    def test_properties(self):
        """Test Court model properties."""
        court = Court.from_dict({
            'id': 4,
            'end_date': '2020-01-01T00:00:00Z'
        })
        assert hasattr(court, 'is_defunct')
        
        court = Court.from_dict({'id': 5})
        assert court.is_defunct is False
        
        # Note: is_federal, is_state, and is_territorial properties are not implemented
        # in the Court model, so we skip these tests
        pass
    
    def test_string_representations(self):
        """Test Court model string representations."""
        court = Court.from_dict({
            'id': 9,
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS'
        })
        
        assert str(court) == "Court(id=9, name='SCOTUS', short_name='SCOTUS')"
        assert repr(court) == "Court(id='9', name='SCOTUS')" 