"""
Tests for OpinionCited model.
"""

import pytest
from courtlistener.models.opinion_cited import OpinionCited


class TestOpinionCited:
    """Test cases for OpinionCited model."""
    
    def test_opinion_cited_creation(self):
        """Test creating an OpinionCited instance."""
        data = {
            "id": 1,
            "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
            "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/456/",
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/opinions-cited/1/",
            "absolute_url": "https://www.courtlistener.com/opinions-cited/1/"
        }
        
        citation = OpinionCited(data)
        
        assert citation.id == 1
        assert citation.citing_opinion == "https://api.courtlistener.com/api/rest/v4/opinions/123/"
        assert citation.cited_opinion == "https://api.courtlistener.com/api/rest/v4/opinions/456/"
        assert citation.date_created == "2023-01-01T00:00:00Z"
        assert citation.date_modified == "2023-01-02T00:00:00Z"
        assert citation.resource_uri == "https://api.courtlistener.com/api/rest/v4/opinions-cited/1/"
        assert citation.absolute_url == "https://www.courtlistener.com/opinions-cited/1/"
    
    def test_opinion_cited_with_none_values(self):
        """Test creating an OpinionCited with None values."""
        data = {
            "id": 1,
            "citing_opinion": None,
            "cited_opinion": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        citation = OpinionCited(data)
        
        assert citation.id == 1
        assert citation.citing_opinion is None
        assert citation.cited_opinion is None
        assert citation.date_created is None
        assert citation.date_modified is None
        assert citation.resource_uri is None
        assert citation.absolute_url is None
