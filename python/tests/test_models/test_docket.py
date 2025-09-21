import pytest
from courtlistener.models.docket import Docket
from datetime import datetime


class TestDocket:
    def test_from_dict_and_to_dict(self):
        """Test Docket model serialization and deserialization."""
        data = {
            'id': 1,
            'docket_number': '21-123',
            'case_name': 'Smith v. Jones',
            'case_name_short': 'Smith',
            'case_name_full': 'John Smith v. Mary Jones',
            'date_filed': '2020-01-01T00:00:00Z',
            'date_terminated': '2021-01-01T00:00:00Z',
            'court': 1,
            'nature_of_suit': 'Civil Rights',
            'jurisdiction_type': 'Federal Question',
            'absolute_url': '/docket/1/',
            'resource_uri': '/api/rest/v4/dockets/1/'
        }
        
        docket = Docket.from_dict(data)
        assert docket.id == 1
        assert docket.docket_number == '21-123'
        assert docket.case_name == 'Smith v. Jones'
        assert docket.case_name_short == 'Smith'
        assert docket.case_name_full == 'John Smith v. Mary Jones'
        assert hasattr(docket, 'date_filed')
        assert hasattr(docket, 'date_terminated')
        assert docket.court == 1
        assert docket.nature_of_suit == 'Civil Rights'
        assert docket.jurisdiction_type == 'Federal Question'
        assert docket.absolute_url == '/docket/1/'
        assert docket.resource_uri == '/api/rest/v4/dockets/1/'
        
        # Test to_dict
        d = docket.to_dict()
        assert d['id'] == 1
        assert d['docket_number'] == '21-123'
        assert d['case_name'] == 'Smith v. Jones'
        assert d['court'] == 1
    
    def test_edge_cases(self):
        """Test Docket model edge cases."""
        # Missing optional fields
        docket = Docket.from_dict({'id': 2})
        assert docket.id == 2
        assert docket.docket_number is None
        assert docket.case_name == 'Unknown Case'
        assert docket.date_filed is None
        assert docket.date_terminated is None
        
        # Invalid dates
        docket = Docket.from_dict({'id': 3, 'date_filed': 'not-a-date'})
        assert docket.date_filed is None
    
    def test_properties(self):
        """Test Docket model properties."""
        docket = Docket.from_dict({
            'id': 4,
            'date_terminated': '2021-01-01T00:00:00Z'
        })
        assert docket.is_terminated is True
        
        docket = Docket.from_dict({'id': 5})
        assert docket.is_terminated is False
    
    def test_string_representations(self):
        """Test Docket model string representations."""
        docket = Docket.from_dict({
            'id': 6,
            'docket_number': '21-123',
            'case_name': 'Smith v. Jones'
        })
        
        assert str(docket) == "Docket(id=6, docket_number='21-123', case_name='Smith v. Jones')"
        assert repr(docket) == "Docket(id=6, case_name='Smith v. Jones')" 