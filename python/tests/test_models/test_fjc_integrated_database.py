"""
Tests for FJCIntegratedDatabase model.
"""

import pytest
from courtlistener.models.fjc_integrated_database import FJCIntegratedDatabase


class TestFJCIntegratedDatabase:
    """Test cases for FJCIntegratedDatabase model."""
    
    def test_fjc_integrated_database_creation(self):
        """Test creating an FJCIntegratedDatabase instance."""
        data = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "position": "Justice",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/fjc-integrated-database/1/",
            "absolute_url": "https://www.courtlistener.com/fjc-integrated-database/1/"
        }
        
        record = FJCIntegratedDatabase(data)
        
        assert record.id == 1
        assert record.person == "https://api.courtlistener.com/api/rest/v4/people/123/"
        assert record.court == "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        assert record.position == "Justice"
        assert record.date_created == "2023-01-01T00:00:00Z"
        assert record.date_modified == "2023-01-02T00:00:00Z"
        assert record.resource_uri == "https://api.courtlistener.com/api/rest/v4/fjc-integrated-database/1/"
        assert record.absolute_url == "https://www.courtlistener.com/fjc-integrated-database/1/"
    
    def test_fjc_integrated_database_with_none_values(self):
        """Test creating an FJCIntegratedDatabase with None values."""
        data = {
            "id": 1,
            "person": None,
            "court": None,
            "position": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        record = FJCIntegratedDatabase(data)
        
        assert record.id == 1
        assert record.person is None
        assert record.court is None
        assert record.position is None
        assert record.date_created is None
        assert record.date_modified is None
        assert record.resource_uri is None
        assert record.absolute_url is None
