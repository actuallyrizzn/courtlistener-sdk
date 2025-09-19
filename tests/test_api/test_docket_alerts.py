"""
Tests for Docket Alerts API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.docket_alerts import DocketAlertsAPI


class TestDocketAlertsAPI:
    """Test cases for Docket Alerts API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = DocketAlertsAPI(self.mock_client)
    
    def test_list_docket_alerts(self):
        """Test listing docket alerts."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
                    "alert_type": "entry",
                    "webhook_url": "https://example.com/webhook"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(docket=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "docket-alerts/",
            params={"docket": 123}
        )
    
    def test_list_with_alert_type_filter(self):
        """Test listing with alert type filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(alert_type="document")
        
        expected_params = {"alert_type": "document"}
        self.mock_client.get.assert_called_once_with("docket-alerts/", params=expected_params)
    
    def test_get_docket_alert(self):
        """Test getting a specific docket alert."""
        mock_response = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "entry"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("docket-alerts/1/")
    
    def test_create_docket_alert(self):
        """Test creating a new docket alert."""
        mock_response = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "entry"
        }
        self.mock_client.post.return_value = mock_response
        
        result = self.api.create(
            docket=123,
            alert_type="entry",
            webhook_url="https://example.com/webhook"
        )
        
        expected_data = {
            "docket": 123,
            "alert_type": "entry",
            "webhook_url": "https://example.com/webhook"
        }
        assert result == mock_response
        self.mock_client.post.assert_called_once_with("docket-alerts/", data=expected_data)
    
    def test_update_docket_alert(self):
        """Test updating a docket alert."""
        mock_response = {
            "id": 1,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/123/",
            "alert_type": "document"
        }
        self.mock_client.post.return_value = mock_response
        
        result = self.api.update(1, alert_type="document")
        
        assert result == mock_response
        self.mock_client.post.assert_called_once_with("docket-alerts/1/", data={"alert_type": "document"})
    
    def test_delete_docket_alert(self):
        """Test deleting a docket alert."""
        self.api.delete(1)
        
        self.mock_client._make_request.assert_called_once_with('DELETE', "docket-alerts/1/")
    
    def test_paginate_docket_alerts(self):
        """Test paginating docket alerts."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(docket=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "docket-alerts/",
            params={"docket": 123}
        )
