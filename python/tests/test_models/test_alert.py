"""
Tests for Alert model.
"""

import pytest
from courtlistener.models.alert import Alert


class TestAlert:
    """Test cases for Alert model."""
    
    def test_alert_creation(self):
        """Test creating an Alert instance."""
        data = {
            "id": 1,
            "name": "Test Alert",
            "query": "constitutional",
            "rate": "wly",
            "alert_type": "search",
            "webhook_url": "https://example.com/webhook",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/alerts/1/",
            "absolute_url": "https://www.courtlistener.com/alerts/1/"
        }
        
        alert = Alert(data)
        
        assert alert.id == 1
        assert alert.name == "Test Alert"
        assert alert.query == "constitutional"
        assert alert.rate == "wly"
        assert alert.alert_type == "search"
        assert alert.webhook_url == "https://example.com/webhook"
        assert alert.date_created == "2023-01-01T00:00:00Z"
        assert alert.date_modified == "2023-01-02T00:00:00Z"
        assert alert.resource_uri == "https://api.courtlistener.com/api/rest/v4/alerts/1/"
        assert alert.absolute_url == "https://www.courtlistener.com/alerts/1/"
    
    def test_alert_with_none_values(self):
        """Test creating an Alert with None values."""
        data = {
            "id": 1,
            "name": None,
            "query": None,
            "rate": None,
            "alert_type": None,
            "webhook_url": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        alert = Alert(data)
        
        assert alert.id == 1
        assert alert.name is None
        assert alert.query is None
        assert alert.rate is None
        assert alert.alert_type is None
        assert alert.webhook_url is None
        assert alert.date_created is None
        assert alert.date_modified is None
        assert alert.resource_uri is None
        assert alert.absolute_url is None
