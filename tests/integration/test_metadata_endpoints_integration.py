"""
Integration tests for Metadata and Utility endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestMetadataEndpointsIntegration:
    """Integration tests for metadata and utility endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_sources_workflow(self):
        """Test sources workflow."""
        # Mock sources list
        mock_sources = {
            "count": 1,
            "results": [{
                "id": 1,
                "name": "Supreme Court Website",
                "type": "Court Website",
                "url": "https://www.supremecourt.gov"
            }]
        }
        self.client.get.return_value = mock_sources
        
        # Test getting sources
        sources = self.client.sources.list()
        assert sources["count"] == 1
        assert len(sources["results"]) == 1
        
        # Test getting specific source
        mock_source = mock_sources["results"][0]
        self.client.get.return_value = mock_source
        
        source = self.client.sources.get(1)
        assert source["name"] == "Supreme Court Website"
    
    def test_retention_events_workflow(self):
        """Test retention events workflow."""
        # Mock retention events list
        mock_events = {
            "count": 1,
            "results": [{
                "id": 1,
                "event_type": "Document Deletion",
                "description": "Documents older than 10 years deleted",
                "date": "2023-01-01"
            }]
        }
        self.client.get.return_value = mock_events
        
        # Test getting retention events
        events = self.client.retention_events.list()
        assert events["count"] == 1
        assert len(events["results"]) == 1
        
        # Test getting specific event
        mock_event = mock_events["results"][0]
        self.client.get.return_value = mock_event
        
        event = self.client.retention_events.get(1)
        assert event["event_type"] == "Document Deletion"
    
    def test_tags_workflow(self):
        """Test tags workflow."""
        # Mock tags list
        mock_tags = {
            "count": 1,
            "results": [{
                "id": 1,
                "name": "Constitutional Law",
                "description": "Cases involving constitutional issues"
            }]
        }
        self.client.get.return_value = mock_tags
        
        # Test getting tags
        tags = self.client.tag.list()
        assert tags["count"] == 1
        assert len(tags["results"]) == 1
        
        # Test getting specific tag
        mock_tag = mock_tags["results"][0]
        self.client.get.return_value = mock_tag
        
        tag = self.client.tag.get(1)
        assert tag["name"] == "Constitutional Law"
    
    def test_originating_court_information_workflow(self):
        """Test originating court information workflow."""
        # Mock originating court information list
        mock_info = {
            "count": 1,
            "results": [{
                "id": 1,
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
                "jurisdiction": "Federal",
                "description": "Supreme Court of the United States"
            }]
        }
        self.client.get.return_value = mock_info
        
        # Test getting originating court information
        info = self.client.originating_court_information.list()
        assert info["count"] == 1
        assert len(info["results"]) == 1
        
        # Test getting specific info
        mock_court_info = mock_info["results"][0]
        self.client.get.return_value = mock_court_info
        
        court_info = self.client.originating_court_information.get(1)
        assert court_info["jurisdiction"] == "Federal"
    
    def test_fjc_integrated_database_workflow(self):
        """Test FJC integrated database workflow."""
        # Mock FJC integrated database list
        mock_records = {
            "count": 1,
            "results": [{
                "id": 1,
                "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
                "position": "Justice"
            }]
        }
        self.client.get.return_value = mock_records
        
        # Test getting FJC integrated database records
        records = self.client.fjc_integrated_database.list()
        assert records["count"] == 1
        assert len(records["results"]) == 1
        
        # Test getting specific record
        mock_record = mock_records["results"][0]
        self.client.get.return_value = mock_record
        
        record = self.client.fjc_integrated_database.get(1)
        assert record["position"] == "Justice"
    
    def test_metadata_endpoints_pagination(self):
        """Test that pagination works for metadata endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        metadata_endpoints = [
            'sources',
            'retention_events',
            'tag',
            'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in metadata_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.paginate()
            assert result == mock_iterator
    
    def test_metadata_endpoints_get_methods(self):
        """Test that get methods work for all metadata endpoints."""
        mock_response = {"id": 1, "name": "Test item"}
        self.client.get.return_value = mock_response
        
        metadata_endpoints = [
            'sources',
            'retention_events',
            'tag',
            'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in metadata_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.get(1)
            assert result == mock_response
