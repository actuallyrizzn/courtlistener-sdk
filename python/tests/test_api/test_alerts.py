"""
Tests for Alerts API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.alerts import AlertsAPI


class TestAlertsAPI:
    """Test cases for Alerts API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = AlertsAPI(self.mock_client)
    
    def test_list_alerts(self):
        """Test listing alerts."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "Test Alert",
                    "query": "constitutional",
                    "rate": "wly"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("alerts/", params={})
    
    def test_list_alerts_with_filters(self):
        """Test listing alerts with filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(name="Test", alert_type="search")
        
        expected_params = {"name": "Test", "alert_type": "search"}
        self.mock_client.get.assert_called_once_with("alerts/", params=expected_params)
    
    def test_get_alert(self):
        """Test getting a specific alert."""
        mock_response = {
            "id": 1,
            "name": "Test Alert",
            "query": "constitutional",
            "rate": "wly"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("alerts/1/")
    
    def test_create_alert(self):
        """Test creating a new alert."""
        mock_response = {
            "id": 1,
            "name": "New Alert",
            "query": "constitutional",
            "rate": "wly"
        }
        self.mock_client.post.return_value = mock_response
        
        result = self.api.create(
            name="New Alert",
            query="constitutional",
            rate="wly",
            alert_type="search"
        )
        
        expected_data = {
            "name": "New Alert",
            "query": "constitutional",
            "rate": "wly",
            "alert_type": "search"
        }
        assert result == mock_response
        self.mock_client.post.assert_called_once_with("alerts/", data=expected_data)
    
    def test_update_alert(self):
        """Test updating an alert."""
        mock_response = {
            "id": 1,
            "name": "Updated Alert",
            "query": "constitutional",
            "rate": "dly"
        }
        self.mock_client.post.return_value = mock_response
        
        result = self.api.update(1, rate="dly")
        
        assert result == mock_response
        self.mock_client.post.assert_called_once_with("alerts/1/", data={"rate": "dly"})
    
    def test_delete_alert(self):
        """Test deleting an alert."""
        self.api.delete(1)
        
        self.mock_client._make_request.assert_called_once_with('DELETE', "alerts/1/")
    
    def test_paginate_alerts(self):
        """Test paginating alerts."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(alert_type="search")
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "alerts/",
            params={"alert_type": "search"}
        )
