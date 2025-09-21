import pytest
from courtlistener.models.citation import Citation
from datetime import datetime


class TestCitation:
    def test_from_dict_and_to_dict(self):
        """Test Citation model serialization and deserialization."""
        data = {
            'id': 1,
            'volume': 410,
            'reporter': 'U.S.',
            'page': 113,
            'type': 'federal',
            'year': 1973,
            'absolute_url': '/citation/1/',
            'resource_uri': '/api/rest/v4/citations/1/'
        }
        
        citation = Citation.from_dict(data)
        assert citation.id == 1
        assert citation.volume == 410
        assert citation.reporter == 'U.S.'
        assert citation.page == 113
        assert citation.type == 'federal'
        assert citation.year == 1973
        assert citation.absolute_url == '/citation/1/'
        assert citation.resource_uri == '/api/rest/v4/citations/1/'
        
        # Test to_dict
        d = citation.to_dict()
        assert d['id'] == 1
        assert d['volume'] == 410
        assert d['reporter'] == 'U.S.'
        assert d['page'] == 113
        assert d['type'] == 'federal'
    
    def test_edge_cases(self):
        """Test Citation model edge cases."""
        # Missing optional fields
        citation = Citation.from_dict({'id': 2})
        assert citation.id == 2
        assert citation.volume is None
        assert citation.reporter is None
        assert citation.page is None
        assert citation.type is None
        assert citation.year is None
        
        # Zero values
        citation = Citation.from_dict({
            'id': 3,
            'volume': 0,
            'page': 0,
            'year': 0
        })
        assert citation.volume == 0
        assert citation.page == 0
        assert citation.year == 0
    
    def test_properties(self):
        """Test Citation model properties."""
        citation = Citation.from_dict({
            'id': 4,
            'volume': 410,
            'reporter': 'U.S.',
            'page': 113
        })
        assert citation.citation_string == '410 U.S. 113'
        
        citation = Citation.from_dict({
            'id': 5,
            'volume': 123,
            'reporter': 'F.3d',
            'page': 456
        })
        assert citation.citation_string == '123 F.3d 456'
        
        citation = Citation.from_dict({
            'id': 6,
            'type': 'federal'
        })
        assert citation.is_federal is True
        
        citation = Citation.from_dict({
            'id': 7,
            'type': 'state'
        })
        assert citation.is_state is True
        
        citation = Citation.from_dict({
            'id': 8,
            'type': 'unknown'
        })
        assert citation.is_federal is False
        assert citation.is_state is False
    
    def test_string_representations(self):
        """Test Citation model string representations."""
        citation = Citation.from_dict({
            'id': 9,
            'volume': 410,
            'reporter': 'U.S.',
            'page': 113,
            'year': 1973
        })
        
        assert str(citation) == "Citation(id=9, citation='410 U.S. 113', year=1973)"
        assert repr(citation) == "Citation(id=9, citation='410 U.S. 113', year=1973)" 