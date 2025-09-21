"""
Tests for RetentionEvent model.
"""

import pytest
from courtlistener.models.retention_event import RetentionEvent


class TestRetentionEvent:
    """Test cases for RetentionEvent model."""
    
    def test_retention_event_creation(self):
        """Test creating a RetentionEvent instance."""
        data = {
            "id": 1,
            "event_type": "Document Deletion",
            "description": "Documents older than 10 years deleted",
            "date": "2023-01-01",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/retention-events/1/",
            "absolute_url": "https://www.courtlistener.com/retention-events/1/"
        }
        
        event = RetentionEvent(data)
        
        assert event.id == 1
        assert event.event_type == "Document Deletion"
        assert event.description == "Documents older than 10 years deleted"
        assert event.date == "2023-01-01"
        assert event.date_created == "2023-01-01T00:00:00Z"
        assert event.date_modified == "2023-01-02T00:00:00Z"
        assert event.resource_uri == "https://api.courtlistener.com/api/rest/v4/retention-events/1/"
        assert event.absolute_url == "https://www.courtlistener.com/retention-events/1/"
    
    def test_retention_event_with_none_values(self):
        """Test creating a RetentionEvent with None values."""
        data = {
            "id": 1,
            "event_type": None,
            "description": None,
            "date": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        event = RetentionEvent(data)
        
        assert event.id == 1
        assert event.event_type is None
        assert event.description is None
        assert event.date is None
        assert event.date_created is None
        assert event.date_modified is None
        assert event.resource_uri is None
        assert event.absolute_url is None
