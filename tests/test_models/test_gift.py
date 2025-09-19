"""
Tests for Gift model.
"""

import pytest
from courtlistener.models.gift import Gift


class TestGift:
    """Test cases for Gift model."""
    
    def test_gift_creation(self):
        """Test creating a Gift instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Conference attendance",
            "value": 2500.0,
            "source": "Legal Foundation",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/gifts/1/",
            "absolute_url": "https://www.courtlistener.com/gifts/1/"
        }
        
        gift = Gift(data)
        
        assert gift.id == 1
        assert gift.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert gift.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert gift.description == "Conference attendance"
        assert gift.value == 2500.0
        assert gift.source == "Legal Foundation"
        assert gift.date_created == "2023-01-01T00:00:00Z"
        assert gift.date_modified == "2023-01-02T00:00:00Z"
        assert gift.resource_uri == "https://api.courtlistener.com/api/rest/v4/gifts/1/"
        assert gift.absolute_url == "https://www.courtlistener.com/gifts/1/"
    
    def test_gift_with_none_values(self):
        """Test creating a Gift with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "value": None,
            "source": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        gift = Gift(data)
        
        assert gift.id == 1
        assert gift.financial_disclosure is None
        assert gift.judge is None
        assert gift.description is None
        assert gift.value is None
        assert gift.source is None
        assert gift.date_created is None
        assert gift.date_modified is None
        assert gift.resource_uri is None
        assert gift.absolute_url is None
