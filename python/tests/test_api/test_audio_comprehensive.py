"""
Comprehensive tests for Audio API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.audio import AudioAPI, Audio
from courtlistener.exceptions import CourtListenerError


class TestAudioAPIComprehensive:
    """Comprehensive tests for AudioAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.mock_client.logger = Mock()
        self.api = AudioAPI(self.mock_client)
    
    def test_init(self):
        """Test AudioAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "audio/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Audio
    
    def test_list_audio_basic(self):
        """Test basic list_audio functionality."""
        mock_response = {
            "results": [
                {"id": 1, "case_name": "Test Case 1"},
                {"id": 2, "case_name": "Test Case 2"}
            ]
        }
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_audio()
        
        assert len(result) == 2
        assert all(isinstance(a, Audio) for a in result)
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/", params={"page": 1})
    
    def test_list_audio_with_page(self):
        """Test list_audio with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.list_audio(page=2)
        
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/", params={"page": 2})
    
    def test_list_audio_with_query(self):
        """Test list_audio with search query."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.list_audio(q="constitutional")
        
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/", params={"page": 1, "q": "constitutional"})
    
    def test_list_audio_with_filters(self):
        """Test list_audio with filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"court": "scotus", "date_filed": "2023-01-01"}
        self.api.list_audio(page=1, **filters)
        
        expected_params = {"page": 1, "court": "scotus", "date_filed": "2023-01-01"}
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/", params=expected_params)
    
    def test_list_audio_with_query_and_filters(self):
        """Test list_audio with both query and filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"court": "scotus"}
        self.api.list_audio(q="constitutional", page=2, **filters)
        
        expected_params = {"page": 2, "q": "constitutional", "court": "scotus"}
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/", params=expected_params)
    
    def test_list_audio_empty_results(self):
        """Test list_audio with empty results."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_audio()
        
        assert result == []
    
    def test_list_audio_no_results_key(self):
        """Test list_audio when response has no results key."""
        mock_response = {}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_audio()
        
        assert result == []
    
    def test_list_audio_exception_handling(self):
        """Test list_audio with exception handling."""
        self.mock_client._make_request.side_effect = Exception("Audio endpoint restricted")
        
        result = self.api.list_audio()
        
        assert result == []
        self.mock_client.logger.warning.assert_called_once_with("Audio endpoint may be restricted: Audio endpoint restricted")
    
    def test_get_audio_success(self):
        """Test get_audio with valid audio ID."""
        mock_response = {"id": 1, "case_name": "Test Case", "duration": 3600}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.get_audio(1)
        
        assert isinstance(result, Audio)
        self.mock_client._make_request.assert_called_once_with("GET", "/audio/1/")
    
    def test_get_audio_not_found(self):
        """Test get_audio with non-existent audio ID."""
        self.mock_client._make_request.side_effect = Exception("Audio not found")
        
        result = self.api.get_audio(999)
        
        assert result is None
        self.mock_client.logger.warning.assert_called_once_with("Could not fetch audio 999: Audio not found")
    
    def test_get_audio_api_error(self):
        """Test get_audio with API error."""
        self.mock_client._make_request.side_effect = CourtListenerError("API Error")
        
        result = self.api.get_audio(1)
        
        assert result is None
        self.mock_client.logger.warning.assert_called_once_with("Could not fetch audio 1: API Error")
    
    def test_search_audio_basic(self):
        """Test search_audio without filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_audio') as mock_list:
            mock_list.return_value = []
            
            result = self.api.search_audio("constitutional")
            
            mock_list.assert_called_once_with(page=1, q="constitutional")
            assert result == []
    
    def test_search_audio_with_page(self):
        """Test search_audio with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_audio') as mock_list:
            mock_list.return_value = []
            
            self.api.search_audio("constitutional", page=2)
            
            mock_list.assert_called_once_with(page=2, q="constitutional")
    
    def test_search_audio_with_filters(self):
        """Test search_audio with filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_audio') as mock_list:
            mock_list.return_value = []
            
            filters = {"court": "scotus"}
            self.api.search_audio("constitutional", page=1, **filters)
            
            mock_list.assert_called_once_with(page=1, q="constitutional", court="scotus")
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError in list_audio."""
        self.mock_client._make_request.side_effect = CourtListenerError("API Error")
        
        result = self.api.list_audio()
        
        assert result == []
        self.mock_client.logger.warning.assert_called_once_with("Audio endpoint may be restricted: API Error")
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors in get_audio."""
        self.mock_client._make_request.side_effect = Exception("Network Error")
        
        result = self.api.get_audio(1)
        
        assert result is None
        self.mock_client.logger.warning.assert_called_once_with("Could not fetch audio 1: Network Error")
