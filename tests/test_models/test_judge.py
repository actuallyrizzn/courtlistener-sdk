import pytest
from courtlistener.models.judge import Judge
from datetime import datetime


class TestJudge:
    def test_from_dict_and_to_dict(self):
        """Test Judge model serialization and deserialization."""
        data = {
            'id': 1,
            'name_first': 'John',
            'name_middle': 'Robert',
            'name_last': 'Smith',
            'name_suffix': 'Jr.',
            'date_dob': '1950-01-01T00:00:00Z',
            'date_dod': '2020-01-01T00:00:00Z',
            'gender': 'M',
            'race': 'White',
            'religion': 'Protestant',
            'political_affiliation': 'Republican',
            'school': 'Harvard Law School',
            'date_start': '1980-01-01T00:00:00Z',
            'date_end': '2020-01-01T00:00:00Z',
            'absolute_url': '/judge/1/',
            'resource_uri': '/api/rest/v4/judges/1/'
        }
        
        judge = Judge.from_dict(data)
        assert judge.id == 1
        assert judge.name_first == 'John'
        assert judge.name_middle == 'Robert'
        assert judge.name_last == 'Smith'
        assert judge.name_suffix == 'Jr.'
        assert isinstance(judge.date_dob, datetime)
        assert isinstance(judge.date_dod, datetime)
        assert judge.gender == 'M'
        assert judge.race == 'White'
        assert judge.religion == 'Protestant'
        assert judge.political_affiliation == 'Republican'
        assert judge.school == 'Harvard Law School'
        assert isinstance(judge.date_start, datetime)
        assert isinstance(judge.date_end, datetime)
        assert judge.absolute_url == '/judge/1/'
        assert judge.resource_uri == '/api/rest/v4/judges/1/'
        
        # Test to_dict
        d = judge.to_dict()
        assert d['id'] == 1
        assert d['name_first'] == 'John'
        assert d['name_last'] == 'Smith'
        assert d['gender'] == 'M'
    
    def test_edge_cases(self):
        """Test Judge model edge cases."""
        # Missing optional fields
        judge = Judge.from_dict({'id': 2})
        assert judge.id == 2
        assert judge.name_first is None
        assert judge.name_last is None
        assert judge.date_dob is None
        assert judge.date_dod is None
        
        # Invalid dates
        judge = Judge.from_dict({'id': 3, 'date_dob': 'not-a-date'})
        assert judge.date_dob is None
    
    def test_properties(self):
        """Test Judge model properties."""
        judge = Judge.from_dict({
            'id': 4,
            'date_dod': '2020-01-01T00:00:00Z'
        })
        assert judge.is_deceased is True
        
        judge = Judge.from_dict({'id': 5})
        assert judge.is_deceased is False
        
        judge = Judge.from_dict({
            'id': 6,
            'date_end': '2020-01-01T00:00:00Z'
        })
        assert judge.is_retired is True
        
        judge = Judge.from_dict({'id': 7})
        assert judge.is_retired is False
    
    def test_full_name(self):
        """Test Judge full name property."""
        judge = Judge.from_dict({
            'id': 8,
            'name_first': 'John',
            'name_middle': 'Robert',
            'name_last': 'Smith',
            'name_suffix': 'Jr.'
        })
        assert judge.full_name == 'John Robert Smith Jr.'
        
        judge = Judge.from_dict({
            'id': 9,
            'name_first': 'Jane',
            'name_last': 'Doe'
        })
        assert judge.full_name == 'Jane Doe'
    
    def test_string_representations(self):
        """Test Judge model string representations."""
        judge = Judge.from_dict({
            'id': 10,
            'name_first': 'John',
            'name_last': 'Smith'
        })
        
        assert str(judge) == "Judge(id=10, name='John Smith')"
        assert repr(judge) == "<Judge(id=10, name_first='John', name_last='Smith', gender=None)>" 