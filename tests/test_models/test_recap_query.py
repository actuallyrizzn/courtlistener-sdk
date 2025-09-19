"""
Tests for RecapQuery model.
"""

import pytest
from courtlistener.models.recap_query import RecapQuery


class TestRecapQuery:
    """Test cases for RecapQuery model."""
    
    def test_recap_query_creation(self):
        """Test creating a RecapQuery instance."""
        data = {
            "id": 1,
            "query": "constitutional law",
            "status": "completed",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/recap-query/1/",
            "absolute_url": "https://www.courtlistener.com/recap-query/1/"
        }
        
        query = RecapQuery(data)
        
        assert query.id == 1
        assert query.query == "constitutional law"
        assert query.status == "completed"
        assert query.date_created == "2023-01-01T00:00:00Z"
        assert query.date_modified == "2023-01-02T00:00:00Z"
        assert query.resource_uri == "https://api.courtlistener.com/api/rest/v4/recap-query/1/"
        assert query.absolute_url == "https://www.courtlistener.com/recap-query/1/"
    
    def test_recap_query_with_none_values(self):
        """Test creating a RecapQuery with None values."""
        data = {
            "id": 1,
            "query": None,
            "status": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        query = RecapQuery(data)
        
        assert query.id == 1
        assert query.query is None
        assert query.status is None
        assert query.date_created is None
        assert query.date_modified is None
        assert query.resource_uri is None
        assert query.absolute_url is None
