"""
Tests for Source model.
"""

import pytest
from courtlistener.models.source import Source


class TestSource:
    """Test cases for Source model."""
    
    def test_source_creation(self):
        """Test creating a Source instance."""
        data = {
            "id": 1,
            "name": "Supreme Court Website",
            "type": "Court Website",
            "url": "https://www.supremecourt.gov",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/sources/1/",
            "absolute_url": "https://www.courtlistener.com/sources/1/"
        }
        
        source = Source(data)
        
        assert source.id == 1
        assert source.name == "Supreme Court Website"
        assert source.type == "Court Website"
        assert source.url == "https://www.supremecourt.gov"
        assert source.date_created == "2023-01-01T00:00:00Z"
        assert source.date_modified == "2023-01-02T00:00:00Z"
        assert source.resource_uri == "https://api.courtlistener.com/api/rest/v4/sources/1/"
        assert source.absolute_url == "https://www.courtlistener.com/sources/1/"
    
    def test_source_with_none_values(self):
        """Test creating a Source with None values."""
        data = {
            "id": 1,
            "name": None,
            "type": None,
            "url": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        source = Source(data)
        
        assert source.id == 1
        assert source.name is None
        assert source.type is None
        assert source.url is None
        assert source.date_created is None
        assert source.date_modified is None
        assert source.resource_uri is None
        assert source.absolute_url is None
