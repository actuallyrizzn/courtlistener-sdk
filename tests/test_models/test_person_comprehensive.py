"""Comprehensive tests for Person model."""

import pytest
from courtlistener.models.person import Person


class TestPersonComprehensive:
    """Comprehensive tests for Person model."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "name": "John Doe"}
        person = Person(data)
        assert person._data == data

    def test_init_sets_all_attributes(self):
        """Test that __init__ sets all expected attributes."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice",
            "birthday": "1950-01-01",
            "education": "Harvard Law",
            "political_affiliation": "Independent",
            "date_created": "2023-01-01T12:00:00Z",
            "date_modified": "2023-01-15T10:30:00Z",
            "resource_uri": "http://api.example.com/person/1/",
            "absolute_url": "http://example.com/person/1"
        }
        person = Person(data)
        
        # Check that all attributes are set correctly
        assert person.id == 1
        assert person.name == "John Doe"
        assert person.court == "scotus"
        assert person.position == "Justice"
        assert person.birthday == "1950-01-01"
        assert person.education == "Harvard Law"
        assert person.political_affiliation == "Independent"
        assert person.date_created == "2023-01-01T12:00:00Z"
        assert person.date_modified == "2023-01-15T10:30:00Z"
        assert person.resource_uri == "http://api.example.com/person/1/"
        assert person.absolute_url == "http://example.com/person/1"

    def test_init_with_none_values(self):
        """Test initialization with None values."""
        data = {}
        person = Person(data)
        
        # All attributes should be None
        assert person.id is None
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

    def test_init_with_partial_data(self):
        """Test initialization with partial data."""
        data = {
            "id": 1,
            "name": "John Doe"
        }
        person = Person(data)
        
        # Set attributes should have values
        assert person.id == 1
        assert person.name == "John Doe"
        
        # Unset attributes should be None
        assert person.court is None
        assert person.position is None
        assert person.birthday is None
        assert person.education is None
        assert person.political_affiliation is None
        assert person.date_created is None
        assert person.date_modified is None
        assert person.resource_uri is None
        assert person.absolute_url is None

    def test_init_with_empty_strings(self):
        """Test initialization with empty strings."""
        data = {
            "id": 1,
            "name": "",
            "court": "",
            "position": "",
            "birthday": "",
            "education": "",
            "political_affiliation": "",
            "date_created": "",
            "date_modified": "",
            "resource_uri": "",
            "absolute_url": ""
        }
        person = Person(data)
        
        # All attributes should be empty strings
        assert person.id == 1
        assert person.name == ""
        assert person.court == ""
        assert person.position == ""
        assert person.birthday == ""
        assert person.education == ""
        assert person.political_affiliation == ""
        assert person.date_created == ""
        assert person.date_modified == ""
        assert person.resource_uri == ""
        assert person.absolute_url == ""

    def test_init_with_zero_id(self):
        """Test initialization with zero id."""
        data = {"id": 0}
        person = Person(data)
        assert person.id == 0

    def test_init_with_negative_id(self):
        """Test initialization with negative id."""
        data = {"id": -1}
        person = Person(data)
        assert person.id == -1

    def test_init_with_large_id(self):
        """Test initialization with large id."""
        data = {"id": 999999999}
        person = Person(data)
        assert person.id == 999999999

    def test_init_with_special_characters(self):
        """Test initialization with special characters in strings."""
        data = {
            "name": "José María",
            "court": "court-123",
            "position": "Chief Justice (Ret.)",
            "education": "Yale Law School, J.D.",
            "political_affiliation": "Non-partisan"
        }
        person = Person(data)
        
        assert person.name == "José María"
        assert person.court == "court-123"
        assert person.position == "Chief Justice (Ret.)"
        assert person.education == "Yale Law School, J.D."
        assert person.political_affiliation == "Non-partisan"

    def test_init_with_unicode_strings(self):
        """Test initialization with unicode strings."""
        data = {
            "name": "张三",
            "court": "最高法院",
            "position": "法官"
        }
        person = Person(data)
        
        assert person.name == "张三"
        assert person.court == "最高法院"
        assert person.position == "法官"

    def test_init_with_numeric_strings(self):
        """Test initialization with numeric strings."""
        data = {
            "id": "123",
            "name": "123",
            "court": "123",
            "position": "123"
        }
        person = Person(data)
        
        # id should be converted to int
        assert person.id == 123
        # Other fields should remain as strings
        assert person.name == "123"
        assert person.court == "123"
        assert person.position == "123"

    def test_comprehensive_data(self):
        """Test with comprehensive data."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice",
            "birthday": "1950-01-01",
            "education": "Harvard Law School",
            "political_affiliation": "Independent",
            "date_created": "2023-01-01T12:00:00Z",
            "date_modified": "2023-01-15T10:30:00Z",
            "resource_uri": "http://api.example.com/person/1/",
            "absolute_url": "http://example.com/person/1"
        }
        person = Person(data)
        
        # Verify all attributes
        assert person.id == 1
        assert person.name == "John Doe"
        assert person.court == "scotus"
        assert person.position == "Justice"
        assert person.birthday == "1950-01-01"
        assert person.education == "Harvard Law School"
        assert person.political_affiliation == "Independent"
        assert person.date_created == "2023-01-01T12:00:00Z"
        assert person.date_modified == "2023-01-15T10:30:00Z"
        assert person.resource_uri == "http://api.example.com/person/1/"
        assert person.absolute_url == "http://example.com/person/1"

    def test_edge_case_empty_data(self):
        """Test with completely empty data."""
        data = {}
        person = Person(data)
        
        # All attributes should be None
        assert person.id is None
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

    def test_edge_case_extra_data(self):
        """Test with extra data not in the model."""
        data = {
            "id": 1,
            "name": "John Doe",
            "extra_field": "extra_value",
            "another_field": 123
        }
        person = Person(data)
        
        # Standard attributes should be set
        assert person.id == 1
        assert person.name == "John Doe"
        
        # Extra fields should not be accessible as attributes
        assert not hasattr(person, 'extra_field')
        assert not hasattr(person, 'another_field')
        
        # But they should be in _data
        assert person._data['extra_field'] == "extra_value"
        assert person._data['another_field'] == 123

    def test_attribute_types(self):
        """Test that attributes have correct types."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice",
            "birthday": "1950-01-01",
            "education": "Harvard Law",
            "political_affiliation": "Independent",
            "date_created": "2023-01-01T12:00:00Z",
            "date_modified": "2023-01-15T10:30:00Z",
            "resource_uri": "http://api.example.com/person/1/",
            "absolute_url": "http://example.com/person/1"
        }
        person = Person(data)
        
        # Check types
        assert isinstance(person.id, int)
        assert isinstance(person.name, str)
        assert isinstance(person.court, str)
        assert isinstance(person.position, str)
        assert isinstance(person.birthday, str)
        assert isinstance(person.education, str)
        assert isinstance(person.political_affiliation, str)
        assert isinstance(person.date_created, str)
        assert isinstance(person.date_modified, str)
        assert isinstance(person.resource_uri, str)
        assert isinstance(person.absolute_url, str)
