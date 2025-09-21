"""
Tests for RecapFetch model.
"""

import pytest
from courtlistener.models.recap_fetch import RecapFetch


class TestRecapFetch:
    """Test cases for RecapFetch model."""
    
    def test_recap_fetch_creation(self):
        """Test creating a RecapFetch instance."""
        data = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "status": "completed",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/recap-fetch/1/",
            "absolute_url": "https://www.courtlistener.com/recap-fetch/1/"
        }
        
        fetch = RecapFetch(data)
        
        assert fetch.id == 1
        assert fetch.docket == "https://api.courtlistener.com/api/rest/v4/dockets/123/"
        assert fetch.status == "completed"
        assert fetch.date_created == "2023-01-01T00:00:00Z"
        assert fetch.date_modified == "2023-01-02T00:00:00Z"
        assert fetch.resource_uri == "https://api.courtlistener.com/api/rest/v4/recap-fetch/1/"
        assert fetch.absolute_url == "https://www.courtlistener.com/recap-fetch/1/"
    
    def test_recap_fetch_with_none_values(self):
        """Test creating a RecapFetch with None values."""
        data = {
            "id": 1,
            "docket": None,
            "status": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        fetch = RecapFetch(data)
        
        assert fetch.id == 1
        assert fetch.docket is None
        assert fetch.status is None
        assert fetch.date_created is None
        assert fetch.date_modified is None
        assert fetch.resource_uri is None
        assert fetch.absolute_url is None
