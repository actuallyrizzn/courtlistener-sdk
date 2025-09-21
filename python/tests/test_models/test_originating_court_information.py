"""
Tests for OriginatingCourtInformation model.
"""

import pytest
from courtlistener.models.originating_court_information import OriginatingCourtInformation


class TestOriginatingCourtInformation:
    """Test cases for OriginatingCourtInformation model."""
    
    def test_originating_court_information_creation(self):
        """Test creating an OriginatingCourtInformation instance."""
        data = {
            "id": 1,
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "jurisdiction": "Federal",
            "description": "Supreme Court of the United States",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/originating-court-information/1/",
            "absolute_url": "https://www.courtlistener.com/originating-court-information/1/"
        }
        
        info = OriginatingCourtInformation(data)
        
        assert info.id == 1
        assert info.court == "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        assert info.jurisdiction == "Federal"
        assert info.description == "Supreme Court of the United States"
        assert info.date_created == "2023-01-01T00:00:00Z"
        assert info.date_modified == "2023-01-02T00:00:00Z"
        assert info.resource_uri == "https://api.courtlistener.com/api/rest/v4/originating-court-information/1/"
        assert info.absolute_url == "https://www.courtlistener.com/originating-court-information/1/"
    
    def test_originating_court_information_with_none_values(self):
        """Test creating an OriginatingCourtInformation with None values."""
        data = {
            "id": 1,
            "court": None,
            "jurisdiction": None,
            "description": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        info = OriginatingCourtInformation(data)
        
        assert info.id == 1
        assert info.court is None
        assert info.jurisdiction is None
        assert info.description is None
        assert info.date_created is None
        assert info.date_modified is None
        assert info.resource_uri is None
        assert info.absolute_url is None
