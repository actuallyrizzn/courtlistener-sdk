"""
Tests for ABARating model.
"""

import pytest
from courtlistener.models.aba_rating import ABARating


class TestABARating:
    """Test cases for ABARating model."""
    
    def test_aba_rating_creation(self):
        """Test creating an ABARating instance."""
        data = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "rating": "Well Qualified",
            "year": 2020,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/aba-ratings/1/",
            "absolute_url": "https://www.courtlistener.com/aba-ratings/1/"
        }
        
        rating = ABARating(data)
        
        assert rating.id == 1
        assert rating.person == "https://api.courtlistener.com/api/rest/v4/people/123/"
        assert rating.rating == "Well Qualified"
        assert rating.year == 2020
        assert rating.date_created == "2023-01-01T00:00:00Z"
        assert rating.date_modified == "2023-01-02T00:00:00Z"
        assert rating.resource_uri == "https://api.courtlistener.com/api/rest/v4/aba-ratings/1/"
        assert rating.absolute_url == "https://www.courtlistener.com/aba-ratings/1/"
    
    def test_aba_rating_with_none_values(self):
        """Test creating an ABARating with None values."""
        data = {
            "id": 1,
            "person": None,
            "rating": None,
            "year": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        rating = ABARating(data)
        
        assert rating.id == 1
        assert rating.person is None
        assert rating.rating is None
        assert rating.year is None
        assert rating.date_created is None
        assert rating.date_modified is None
        assert rating.resource_uri is None
        assert rating.absolute_url is None
