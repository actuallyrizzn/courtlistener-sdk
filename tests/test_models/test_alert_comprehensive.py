"""Comprehensive tests for Alert model."""

import pytest
from courtlistener.models.alert import Alert


class TestAlertComprehensive:
    """Comprehensive tests for Alert model."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "name": "Test Alert"}
        alert = Alert(data)
        assert alert._data == data

    def test_id_property(self):
        """Test id property."""
        data = {"id": 123}
        alert = Alert(data)
        assert alert.id == 123

    def test_id_property_none(self):
        """Test id property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.id is None

    def test_name_property(self):
        """Test name property."""
        data = {"name": "Test Alert"}
        alert = Alert(data)
        assert alert.name == "Test Alert"

    def test_name_property_none(self):
        """Test name property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.name is None

    def test_query_property(self):
        """Test query property."""
        data = {"query": "test query"}
        alert = Alert(data)
        assert alert.query == "test query"

    def test_query_property_none(self):
        """Test query property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.query is None

    def test_rate_property(self):
        """Test rate property."""
        data = {"rate": "daily"}
        alert = Alert(data)
        assert alert.rate == "daily"

    def test_rate_property_none(self):
        """Test rate property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.rate is None

    def test_alert_type_property(self):
        """Test alert_type property."""
        data = {"alert_type": "search"}
        alert = Alert(data)
        assert alert.alert_type == "search"

    def test_alert_type_property_none(self):
        """Test alert_type property when None."""
        data = {}
        alert = Alert(data)
        assert alert.alert_type is None

    def test_webhook_url_property(self):
        """Test webhook_url property."""
        data = {"webhook_url": "https://example.com/webhook"}
        alert = Alert(data)
        assert alert.webhook_url == "https://example.com/webhook"

    def test_date_created_property(self):
        """Test date_created property."""
        data = {"date_created": "2023-01-01T12:00:00Z"}
        alert = Alert(data)
        assert alert.date_created == "2023-01-01T12:00:00Z"

    def test_date_created_property_none(self):
        """Test date_created property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.date_created is None

    def test_date_modified_property(self):
        """Test date_modified property."""
        data = {"date_modified": "2023-01-15T10:30:00Z"}
        alert = Alert(data)
        assert alert.date_modified == "2023-01-15T10:30:00Z"

    def test_date_modified_property_none(self):
        """Test date_modified property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.date_modified is None

    def test_absolute_url_property(self):
        """Test absolute_url property."""
        data = {"absolute_url": "http://example.com/alert/1"}
        alert = Alert(data)
        assert alert.absolute_url == "http://example.com/alert/1"

    def test_absolute_url_property_none(self):
        """Test absolute_url property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.absolute_url is None

    def test_resource_uri_property(self):
        """Test resource_uri property."""
        data = {"resource_uri": "http://api.example.com/alert/1/"}
        alert = Alert(data)
        assert alert.resource_uri == "http://api.example.com/alert/1/"

    def test_resource_uri_property_none(self):
        """Test resource_uri property when not set."""
        data = {}
        alert = Alert(data)
        assert alert.resource_uri is None

    def test_comprehensive_data(self):
        """Test with comprehensive data."""
        data = {
            "id": 1,
            "name": "Test Alert",
            "query": "test query",
            "rate": "daily",
            "alert_type": "search",
            "webhook_url": "https://example.com/webhook",
            "date_created": "2023-01-01T12:00:00Z",
            "date_modified": "2023-01-15T10:30:00Z",
            "absolute_url": "http://example.com/alert/1",
            "resource_uri": "http://api.example.com/alert/1/"
        }
        alert = Alert(data)
        
        # Test all properties
        assert alert.id == 1
        assert alert.name == "Test Alert"
        assert alert.query == "test query"
        assert alert.rate == "daily"
        assert alert.alert_type == "search"
        assert alert.webhook_url == "https://example.com/webhook"
        assert hasattr(alert, 'date_created')
        assert hasattr(alert, 'date_modified')
        assert alert.absolute_url == "http://example.com/alert/1"
        assert alert.resource_uri == "http://api.example.com/alert/1/"

    def test_edge_case_empty_data(self):
        """Test with completely empty data."""
        data = {}
        alert = Alert(data)
        
        # All properties should be None
        assert alert.id is None
        assert alert.name is None
        assert alert.query is None
        assert alert.rate is None
        assert alert.alert_type is None
        assert alert.webhook_url is None
        assert hasattr(alert, 'date_created')
        assert hasattr(alert, 'date_modified')
        assert alert.absolute_url is None
        assert alert.resource_uri is None

    def test_edge_case_partial_data(self):
        """Test with partial data."""
        data = {"id": 1, "name": "Test Alert"}
        alert = Alert(data)
        
        # Set properties should have values
        assert alert.id == 1
        assert alert.name == "Test Alert"
        
        # Unset properties should be None
        assert alert.query is None
        assert alert.rate is None
        assert alert.alert_type is None
        assert alert.webhook_url is None
        assert hasattr(alert, 'date_created')
        assert alert.date_modified is None
        assert alert.absolute_url is None
        assert alert.resource_uri is None
