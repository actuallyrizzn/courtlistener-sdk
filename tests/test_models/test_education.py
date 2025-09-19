"""
Tests for Education model.
"""

import pytest
from courtlistener.models.education import Education


class TestEducation:
    """Test cases for Education model."""
    
    def test_education_creation(self):
        """Test creating an Education instance."""
        data = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "school": "https://api.courtlistener.com/api/rest/v4/schools/456/",
            "degree": "J.D.",
            "year": 1990,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/educations/1/",
            "absolute_url": "https://www.courtlistener.com/educations/1/"
        }
        
        education = Education(data)
        
        assert education.id == 1
        assert education.person == "https://api.courtlistener.com/api/rest/v4/people/123/"
        assert education.school == "https://api.courtlistener.com/api/rest/v4/schools/456/"
        assert education.degree == "J.D."
        assert education.year == 1990
        assert education.date_created == "2023-01-01T00:00:00Z"
        assert education.date_modified == "2023-01-02T00:00:00Z"
        assert education.resource_uri == "https://api.courtlistener.com/api/rest/v4/educations/1/"
        assert education.absolute_url == "https://www.courtlistener.com/educations/1/"
    
    def test_education_with_none_values(self):
        """Test creating an Education with None values."""
        data = {
            "id": 1,
            "person": None,
            "school": None,
            "degree": None,
            "year": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        education = Education(data)
        
        assert education.id == 1
        assert education.person is None
        assert education.school is None
        assert education.degree is None
        assert education.year is None
        assert education.date_created is None
        assert education.date_modified is None
        assert education.resource_uri is None
        assert education.absolute_url is None
