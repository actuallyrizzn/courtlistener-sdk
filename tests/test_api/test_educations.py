"""
Tests for Educations API.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.educations import EducationsAPI


class TestEducationsAPI:
    """Test cases for Educations API."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = EducationsAPI(self.mock_client)
    
    def test_list_educations(self):
        """Test listing education records."""
        mock_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "school": "https://api.courtlistener.com/api/rest/v4/schools/456/",
                    "degree": "J.D.",
                    "year": 1990
                }
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(person=123)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with(
            "educations/",
            params={"person": 123}
        )
    
    def test_list_with_school_filter(self):
        """Test listing with school filter."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list(school=456)
        
        expected_params = {"school": 456}
        self.mock_client.get.assert_called_once_with("educations/", params=expected_params)
    
    def test_get_education(self):
        """Test getting a specific education record."""
        mock_response = {
            "id": 1,
            "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
            "degree": "J.D."
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get(1)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("educations/1/")
    
    def test_paginate_educations(self):
        """Test paginating education records."""
        mock_iterator = Mock()
        self.mock_client.paginate.return_value = mock_iterator
        
        result = self.api.paginate(person=123)
        
        assert result == mock_iterator
        self.mock_client.paginate.assert_called_once_with(
            "educations/",
            params={"person": 123}
        )
