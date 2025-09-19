"""
Tests for School model.
"""

import pytest
from courtlistener.models.school import School


class TestSchool:
    """Test cases for School model."""
    
    def test_school_creation(self):
        """Test creating a School instance."""
        data = {
            "id": 1,
            "name": "Harvard Law School",
            "type": "Law School",
            "location": "Cambridge, MA",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/schools/1/",
            "absolute_url": "https://www.courtlistener.com/schools/1/"
        }
        
        school = School(data)
        
        assert school.id == 1
        assert school.name == "Harvard Law School"
        assert school.type == "Law School"
        assert school.location == "Cambridge, MA"
        assert school.date_created == "2023-01-01T00:00:00Z"
        assert school.date_modified == "2023-01-02T00:00:00Z"
        assert school.resource_uri == "https://api.courtlistener.com/api/rest/v4/schools/1/"
        assert school.absolute_url == "https://www.courtlistener.com/schools/1/"
    
    def test_school_with_none_values(self):
        """Test creating a School with None values."""
        data = {
            "id": 1,
            "name": None,
            "type": None,
            "location": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        school = School(data)
        
        assert school.id == 1
        assert school.name is None
        assert school.type is None
        assert school.location is None
        assert school.date_created is None
        assert school.date_modified is None
        assert school.resource_uri is None
        assert school.absolute_url is None
