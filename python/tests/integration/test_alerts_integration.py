"""
Integration tests for Alerts and Docket Alerts endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestAlertsIntegration:
    """Integration tests for alerts endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_alerts_crud_workflow(self):
        """Test complete alerts CRUD workflow."""
        # Mock creating an alert
        mock_created_alert = {
            "id": 1,
            "name": "Test Alert",
            "query": "constitutional",
            "rate": "wly",
            "alert_type": "search"
        }
        self.client.post.return_value = mock_created_alert
        
        # Test creating an alert
        alert = self.client.alerts.create(
            name="Test Alert",
            query="constitutional",
            rate="wly",
            alert_type="search"
        )
        assert alert["id"] == 1
        assert alert["name"] == "Test Alert"
        
        # Mock listing alerts
        mock_alerts_list = {
            "count": 1,
            "results": [mock_created_alert]
        }
        self.client.get.return_value = mock_alerts_list
        
        # Test listing alerts
        alerts = self.client.alerts.list()
        assert alerts["count"] == 1
        assert len(alerts["results"]) == 1
        
        # Mock updating an alert
        mock_updated_alert = {
            "id": 1,
            "name": "Updated Alert",
            "query": "constitutional",
            "rate": "dly",
            "alert_type": "search"
        }
        self.client.post.return_value = mock_updated_alert
        
        # Test updating an alert
        updated_alert = self.client.alerts.update(1, rate="dly")
        assert updated_alert["rate"] == "dly"
        
        # Mock getting specific alert
        self.client.get.return_value = mock_updated_alert
        
        # Test getting specific alert
        specific_alert = self.client.alerts.get(1)
        assert specific_alert["id"] == 1
        
        # Test deleting an alert
        self.client.alerts.delete(1)
        self.client._make_request.assert_called_with('DELETE', "alerts/1/")
    
    def test_docket_alerts_crud_workflow(self):
        """Test complete docket alerts CRUD workflow."""
        # Mock creating a docket alert
        mock_created_docket_alert = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "entry"
        }
        self.client.post.return_value = mock_created_docket_alert
        
        # Test creating a docket alert
        docket_alert = self.client.docket_alerts.create(
            docket=123,
            alert_type="entry"
        )
        assert docket_alert["id"] == 1
        assert docket_alert["docket"] == "https://api.courtlistener.com/api/rest/v4/dockets/123/"
        
        # Mock listing docket alerts
        mock_docket_alerts_list = {
            "count": 1,
            "results": [mock_created_docket_alert]
        }
        self.client.get.return_value = mock_docket_alerts_list
        
        # Test listing docket alerts
        docket_alerts = self.client.docket_alerts.list(docket=123)
        assert docket_alerts["count"] == 1
        assert len(docket_alerts["results"]) == 1
        
        # Mock updating a docket alert
        mock_updated_docket_alert = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "document"
        }
        self.client.post.return_value = mock_updated_docket_alert
        
        # Test updating a docket alert
        updated_docket_alert = self.client.docket_alerts.update(1, alert_type="document")
        assert updated_docket_alert["alert_type"] == "document"
        
        # Test deleting a docket alert
        self.client.docket_alerts.delete(1)
        self.client._make_request.assert_called_with('DELETE', "docket-alerts/1/")
    
    def test_alerts_pagination(self):
        """Test that pagination works for alerts endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        # Test alerts pagination
        alerts_iterator = self.client.alerts.paginate(alert_type="search")
        assert alerts_iterator == mock_iterator
        
        # Test docket alerts pagination
        docket_alerts_iterator = self.client.docket_alerts.paginate(docket=123)
        assert docket_alerts_iterator == mock_iterator
    
    def test_alerts_filtering(self):
        """Test that filtering works for alerts endpoints."""
        mock_response = {"count": 0, "results": []}
        self.client.get.return_value = mock_response
        
        # Test alerts filtering
        self.client.alerts.list(name="Test", alert_type="search")
        self.client.get.assert_called_with("alerts/", params={"name": "Test", "alert_type": "search"})
        
        # Test docket alerts filtering
        self.client.docket_alerts.list(docket=123, alert_type="entry")
        self.client.get.assert_called_with("docket-alerts/", params={"docket": 123, "alert_type": "entry"})
