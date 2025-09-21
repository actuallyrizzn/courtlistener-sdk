"""
Tests for Tag model.
"""

import pytest
from courtlistener.models.tag import Tag


class TestTag:
    """Test cases for Tag model."""
    
    def test_tag_creation(self):
        """Test creating a Tag instance."""
        data = {
            "id": 1,
            "name": "Constitutional Law",
            "description": "Cases involving constitutional issues",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/tag/1/",
            "absolute_url": "https://www.courtlistener.com/tag/1/"
        }
        
        tag = Tag(data)
        
        assert tag.id == 1
        assert tag.name == "Constitutional Law"
        assert tag.description == "Cases involving constitutional issues"
        assert tag.date_created == "2023-01-01T00:00:00Z"
        assert tag.date_modified == "2023-01-02T00:00:00Z"
        assert tag.resource_uri == "https://api.courtlistener.com/api/rest/v4/tag/1/"
        assert tag.absolute_url == "https://www.courtlistener.com/tag/1/"
    
    def test_tag_with_none_values(self):
        """Test creating a Tag with None values."""
        data = {
            "id": 1,
            "name": None,
            "description": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        tag = Tag(data)
        
        assert tag.id == 1
        assert tag.name is None
        assert tag.description is None
        assert tag.date_created is None
        assert tag.date_modified is None
        assert tag.resource_uri is None
        assert tag.absolute_url is None
