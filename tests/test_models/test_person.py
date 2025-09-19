"""
Tests for Person model.
"""

import pytest
from courtlistener.models.person import Person


class TestPerson:
    """Test cases for Person model."""
    
    def test_person_creation(self):
        """Test creating a Person instance."""
        data = {
            "id": 1,
            "name": "John Smith",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "position": "Justice",
            "birthday": "1950-01-01",
            "education": "Harvard Law School",
            "political_affiliation": "Republican",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/people/1/",
            "absolute_url": "https://www.courtlistener.com/people/1/"
        }
        
        person = Person(data)
        
        assert person.id == 1
        assert person.name == "John Smith"
        assert person.court == "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        assert person.position == "Justice"
        assert person.birthday == "1950-01-01"
        assert person.education == "Harvard Law School"
        assert person.political_affiliation == "Republican"
        assert person.date_created == "2023-01-01T00:00:00Z"
        assert person.date_modified == "2023-01-02T00:00:00Z"
        assert person.resource_uri == "https://api.courtlistener.com/api/rest/v4/people/1/"
        assert person.absolute_url == "https://www.courtlistener.com/people/1/"
    
    def test_person_with_none_values(self):
        """Test creating a Person with None values."""
        data = {
            "id": 1,
            "name": None,
            "court": None,
            "position": None,
            "birthday": None,
            "education": None,
            "political_affiliation": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        person = Person(data)
        
        assert person.id == 1
        assert person.name is None
        assert person.court is None
        assert person.position is None
        assert person.birthday is None
        assert person.education is None
        assert person.political_affiliation is None
        assert person.date_created is None
        assert person.date_modified is None
        assert person.resource_uri is None
        assert person.absolute_url is None
