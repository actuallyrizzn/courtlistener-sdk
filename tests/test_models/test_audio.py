import pytest
from courtlistener.models.audio import Audio
from datetime import datetime


class TestAudio:
    def test_from_dict_and_to_dict(self):
        """Test Audio model serialization and deserialization."""
        data = {
            'id': 1,
            'docket': 1,
            'docket_entry': 1,
            'source': 'oral_argument',
            'filepath_local': '/path/to/audio.mp3',
            'filepath_ia': 'https://archive.org/audio.mp3',
            'filepath_ia_json': 'https://archive.org/audio.json',
            'duration': 3600,
            'absolute_url': '/audio/1/',
            'resource_uri': '/api/rest/v4/audio/1/'
        }
        
        audio = Audio.from_dict(data)
        assert audio.id == 1
        assert audio.docket == 1
        assert audio.docket_entry == 1
        assert audio.source == 'oral_argument'
        assert audio.filepath_local == '/path/to/audio.mp3'
        assert audio.filepath_ia == 'https://archive.org/audio.mp3'
        assert audio.filepath_ia_json == 'https://archive.org/audio.json'
        assert audio.duration == 3600
        assert audio.absolute_url == '/audio/1/'
        assert audio.resource_uri == '/api/rest/v4/audio/1/'
        
        # Test to_dict
        d = audio.to_dict()
        assert d['id'] == 1
        assert d['docket'] == 1
        assert d['source'] == 'oral_argument'
        assert d['duration'] == 3600
    
    def test_edge_cases(self):
        """Test Audio model edge cases."""
        # Missing optional fields
        audio = Audio.from_dict({'id': 2})
        assert audio.id == 2
        assert audio.docket is None
        assert audio.docket_entry is None
        assert audio.source is None
        assert audio.filepath_local is None
        assert audio.duration is None
        
        # Zero duration
        audio = Audio.from_dict({
            'id': 3,
            'duration': 0
        })
        assert audio.duration == 0
    
    def test_properties(self):
        """Test Audio model properties."""
        audio = Audio.from_dict({
            'id': 4,
            'filepath_local': '/path/to/audio.mp3'
        })
        assert audio.has_local_file is True
        
        audio = Audio.from_dict({'id': 5})
        assert audio.has_local_file is False
        
        audio = Audio.from_dict({
            'id': 6,
            'filepath_ia': 'https://archive.org/audio.mp3'
        })
        assert audio.has_ia_file is True
        
        audio = Audio.from_dict({'id': 7})
        assert audio.has_ia_file is False
        
        audio = Audio.from_dict({
            'id': 8,
            'source': 'oral_argument'
        })
        assert audio.is_oral_argument is True
        
        audio = Audio.from_dict({
            'id': 9,
            'source': 'other'
        })
        assert audio.is_oral_argument is False
    
    def test_duration_formatted(self):
        """Test Audio duration formatting."""
        audio = Audio.from_dict({
            'id': 10,
            'duration': 3661  # 1 hour, 1 minute, 1 second
        })
        assert audio.duration_formatted == '1:01:01'
        
        audio = Audio.from_dict({
            'id': 11,
            'duration': 125  # 2 minutes, 5 seconds
        })
        assert audio.duration_formatted == '0:02:05'
        
        audio = Audio.from_dict({
            'id': 12,
            'duration': 30  # 30 seconds
        })
        assert audio.duration_formatted == '0:00:30'
        
        audio = Audio.from_dict({'id': 13})
        assert audio.duration_formatted == '0:00:00'
    
    def test_string_representations(self):
        """Test Audio model string representations."""
        audio = Audio.from_dict({
            'id': 14,
            'source': 'oral_argument',
            'duration': 3600
        })
        
        assert str(audio) == "Audio(id=14, source='oral_argument', duration=3600)"
        assert repr(audio) == "<Audio(id=14, docket=None, source='oral_argument', duration=3600)>" 