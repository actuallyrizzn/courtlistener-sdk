"""
Comprehensive tests for the Person model class.
"""

import pytest
from courtlistener.models.person import Person


class TestPerson:
    """Test cases for Person class."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice"
        }
        person = Person(data)
        assert person.id == 1
        assert person.name == "John Doe"
        assert person.court == "scotus"
        assert person.position == "Justice"

    def test_init_with_all_fields(self):
        """Test initialization with all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice",
            "birthday": "1950-01-01",
            "education": "Harvard Law School",
            "political_affiliation": "Independent",
            "date_created": "2023-01-01T12:00:00",
            "date_modified": "2023-01-02T12:00:00",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/people/1/",
            "absolute_url": "https://www.courtlistener.com/person/1/"
        }
        person = Person(data)
        assert person.id == 1
        assert person.name == "John Doe"
        assert person.court == "scotus"
        assert person.position == "Justice"
        assert person.birthday == "1950-01-01"
        assert person.education == "Harvard Law School"
        assert person.political_affiliation == "Independent"
        assert person.date_created == "2023-01-01T12:00:00"
        assert person.date_modified == "2023-01-02T12:00:00"
        assert person.resource_uri == "https://api.courtlistener.com/api/rest/v4/people/1/"
        assert person.absolute_url == "https://www.courtlistener.com/person/1/"

    def test_init_with_missing_fields(self):
        """Test initialization with missing fields."""
        data = {"id": 1}
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

    def test_init_with_empty_data(self):
        """Test initialization with empty data."""
        data = {}
        person = Person(data)
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

    def test_init_with_none_values(self):
        """Test initialization with None values."""
        data = {
            "id": None,
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
            "name": "John Doe",
            "birthday": "1950-01-01"
        }
        person = Person(data)
        assert person.id == 1
        assert person.name == "John Doe"
        assert person.birthday == "1950-01-01"
        # Other fields should be None
        assert person.court is None
        assert person.position is None
        assert person.education is None
        assert person.political_affiliation is None
        assert person.date_created is None
        assert person.date_modified is None
        assert person.resource_uri is None
        assert person.absolute_url is None

    def test_inherits_from_base_model(self):
        """Test that Person inherits from BaseModel."""
        data = {"id": 1, "name": "John Doe"}
        person = Person(data)
        assert hasattr(person, 'to_dict')
        assert hasattr(person, 'to_json')
        assert hasattr(person, 'get')
        assert hasattr(person, '__getitem__')
        assert hasattr(person, '__contains__')
        assert hasattr(person, '__repr__')
        assert hasattr(person, '__str__')

    def test_to_dict_includes_all_fields(self):
        """Test that to_dict includes all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus",
            "position": "Justice"
        }
        person = Person(data)
        result = person.to_dict()
        assert result["id"] == 1
        assert result["name"] == "John Doe"
        assert result["court"] == "scotus"
        assert result["position"] == "Justice"

    def test_to_dict_with_none_values(self):
        """Test to_dict with None values."""
        data = {"id": 1}
        person = Person(data)
        result = person.to_dict()
        assert result["id"] == 1
        assert result["name"] is None
        assert result["court"] is None
        assert result["position"] is None

    def test_repr_with_id(self):
        """Test __repr__ with id."""
        data = {"id": 1, "name": "John Doe"}
        person = Person(data)
        # Should use BaseModel's __repr__ which shows id
        assert "Person(id=1)" in repr(person)

    def test_repr_without_id(self):
        """Test __repr__ without id."""
        data = {"name": "John Doe"}
        person = Person(data)
        # BaseModel.__repr__ uses name if id is not available
        result = repr(person)
        assert "Person" in result
        # Should contain name since it's available, or be Person() if name is None
        assert "name" in result or result == "Person()"

    def test_str_uses_repr(self):
        """Test that __str__ uses __repr__."""
        data = {"id": 1, "name": "John Doe"}
        person = Person(data)
        assert str(person) == repr(person)

    def test_get_method_works(self):
        """Test that get method works for all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus"
        }
        person = Person(data)
        assert person.get("id") == 1
        assert person.get("name") == "John Doe"
        assert person.get("court") == "scotus"
        assert person.get("position") is None
        assert person.get("missing", "default") == "default"

    def test_getitem_works(self):
        """Test that __getitem__ works for all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus"
        }
        person = Person(data)
        assert person["id"] == 1
        assert person["name"] == "John Doe"
        assert person["court"] == "scotus"

    def test_contains_works(self):
        """Test that __contains__ works for all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "court": "scotus"
        }
        person = Person(data)
        assert "id" in person
        assert "name" in person
        assert "court" in person
        assert "position" not in person
        assert "missing" not in person