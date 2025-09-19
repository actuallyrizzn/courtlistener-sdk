"""
Tests for People API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.people import PeopleAPI


class TestPeopleAPI:
    """Test cases for People API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = PeopleAPI(self.mock_client)
    
    def test_list_people(self):
        """Test listing people."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "John Smith",
                    "position": "Judge"
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("people/", params={})
    
    def test_list_people_with_filters(self):
        """Test listing people with filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(
            name__icontains="Smith",
            position_type="Judge",
            active=True
        )
        
        expected_params = {
            "name__icontains": "Smith",
            "position_type": "Judge",
            "active": True
        }
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
    
    def test_get_person(self):
        """Test getting a specific person."""
        mock_response = {
            "id": 1,
            "name": "John Smith",
            "position": "Judge",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("people/1/")
    
    def test_paginate_people(self):
        """Test paginating people."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(position_type="Judge")
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "people/",
            params={"position_type": "Judge"}
        )
