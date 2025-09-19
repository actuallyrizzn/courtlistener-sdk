"""
Tests for PoliticalAffiliation model.
"""

import pytest
from courtlistener.models.political_affiliation import PoliticalAffiliation


class TestPoliticalAffiliation:
    """Test cases for PoliticalAffiliation model."""
    
    def test_political_affiliation_creation(self):
        """Test creating a PoliticalAffiliation instance."""
        data = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "party": "Republican",
            "year": 2020,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/political-affiliations/1/",
            "absolute_url": "https://www.courtlistener.com/political-affiliations/1/"
        }
        
        affiliation = PoliticalAffiliation(data)
        
        assert affiliation.id == 1
        assert affiliation.person == "https://api.courtlistener.com/api/rest/v4/people/123/"
        assert affiliation.party == "Republican"
        assert affiliation.year == 2020
        assert affiliation.date_created == "2023-01-01T00:00:00Z"
        assert affiliation.date_modified == "2023-01-02T00:00:00Z"
        assert affiliation.resource_uri == "https://api.courtlistener.com/api/rest/v4/political-affiliations/1/"
        assert affiliation.absolute_url == "https://www.courtlistener.com/political-affiliations/1/"
    
    def test_political_affiliation_with_none_values(self):
        """Test creating a PoliticalAffiliation with None values."""
        data = {
            "id": 1,
            "person": None,
            "party": None,
            "year": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        affiliation = PoliticalAffiliation(data)
        
        assert affiliation.id == 1
        assert affiliation.person is None
        assert affiliation.party is None
        assert affiliation.year is None
        assert affiliation.date_created is None
        assert affiliation.date_modified is None
        assert affiliation.resource_uri is None
        assert affiliation.absolute_url is None
