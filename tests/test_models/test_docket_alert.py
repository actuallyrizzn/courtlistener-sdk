"""
Tests for DocketAlert model.
"""

import pytest
from courtlistener.models.docket_alert import DocketAlert


class TestDocketAlert:
    """Test cases for DocketAlert model."""
    
    def test_docket_alert_creation(self):
        """Test creating a DocketAlert instance."""
        data = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "entry",
            "webhook_url": "https://example.com/webhook",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/docket-alerts/1/",
            "absolute_url": "https://www.courtlistener.com/docket-alerts/1/"
        }
        
        alert = DocketAlert(data)
        
        assert alert.id == 1
        assert alert.docket == "https://api.courtlistener.com/api/rest/v4/dockets/123/"
        assert alert.alert_type == "entry"
        assert alert.webhook_url == "https://example.com/webhook"
        assert alert.date_created == "2023-01-01T00:00:00Z"
        assert alert.date_modified == "2023-01-02T00:00:00Z"
        assert alert.resource_uri == "https://api.courtlistener.com/api/rest/v4/docket-alerts/1/"
        assert alert.absolute_url == "https://www.courtlistener.com/docket-alerts/1/"
    
    def test_docket_alert_with_none_values(self):
        """Test creating a DocketAlert with None values."""
        data = {
            "id": 1,
            "docket": None,
            "alert_type": None,
            "webhook_url": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        alert = DocketAlert(data)
        
        assert alert.id == 1
        assert alert.docket is None
        assert alert.alert_type is None
        assert alert.webhook_url is None
        assert alert.date_created is None
        assert alert.date_modified is None
        assert alert.resource_uri is None
        assert alert.absolute_url is None
