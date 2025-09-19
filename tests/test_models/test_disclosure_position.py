"""
Tests for DisclosurePosition model.
"""

import pytest
from courtlistener.models.disclosure_position import DisclosurePosition


class TestDisclosurePosition:
    """Test cases for DisclosurePosition model."""
    
    def test_disclosure_position_creation(self):
        """Test creating a DisclosurePosition instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "position": "Board Member",
            "organization": "Legal Foundation",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/disclosure-positions/1/",
            "absolute_url": "https://www.courtlistener.com/disclosure-positions/1/"
        }
        
        position = DisclosurePosition(data)
        
        assert position.id == 1
        assert position.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert position.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert position.position == "Board Member"
        assert position.organization == "Legal Foundation"
        assert position.date_created == "2023-01-01T00:00:00Z"
        assert position.date_modified == "2023-01-02T00:00:00Z"
        assert position.resource_uri == "https://api.courtlistener.com/api/rest/v4/disclosure-positions/1/"
        assert position.absolute_url == "https://www.courtlistener.com/disclosure-positions/1/"
    
    def test_disclosure_position_with_none_values(self):
        """Test creating a DisclosurePosition with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "position": None,
            "organization": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        position = DisclosurePosition(data)
        
        assert position.id == 1
        assert position.financial_disclosure is None
        assert position.judge is None
        assert position.position is None
        assert position.organization is None
        assert position.date_created is None
        assert position.date_modified is None
        assert position.resource_uri is None
        assert position.absolute_url is None
