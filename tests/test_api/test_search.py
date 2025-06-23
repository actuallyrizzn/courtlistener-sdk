import pytest
from unittest.mock import Mock, patch
from courtlistener.api.search import SearchAPI
from courtlistener.exceptions import CourtListenerError


class TestSearchAPI:
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.search_api = SearchAPI(self.client)
    
    def test_search_opinions(self):
        """Test searching opinions."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'case_name': 'Test Case'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_opinions(
            q='test query',
            court='scotus',
            date_filed_min='2020-01-01',
            date_filed_max='2021-01-01'
        )
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={
                'q': 'test query',
                'court': 'scotus',
                'date_filed_min': '2020-01-01',
                'date_filed_max': '2021-01-01'
            }
        )
        assert result == mock_response
    
    def test_search_opinions_with_filters(self):
        """Test searching opinions with filters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        filters = {
            'type': '010combined',
            'author': 1,
            'joined_by': [2, 3]
        }
        
        result = self.search_api.search_opinions(filters=filters)
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params=filters
        )
        assert result == mock_response
    
    def test_search_dockets(self):
        """Test searching dockets."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'docket_number': '21-123'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_dockets(
            q='test query',
            court='ca1',
            date_filed_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            '/dockets/',
            params={
                'q': 'test query',
                'court': 'ca1',
                'date_filed_min': '2020-01-01'
            }
        )
        assert result == mock_response
    
    def test_search_documents(self):
        """Test searching documents."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'document_type': 'motion'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_documents(
            q='test query',
            docket=1,
            document_type='motion'
        )
        
        self.client.get.assert_called_once_with(
            '/documents/',
            params={
                'q': 'test query',
                'docket': 1,
                'document_type': 'motion'
            }
        )
        assert result == mock_response
    
    def test_search_audio(self):
        """Test searching audio."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'source': 'oral_argument'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_audio(
            docket=1,
            source='oral_argument'
        )
        
        self.client.get.assert_called_once_with(
            '/audio/',
            params={
                'docket': 1,
                'source': 'oral_argument'
            }
        )
        assert result == mock_response
    
    def test_search_people(self):
        """Test searching people (judges, attorneys, parties)."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'name': 'John Smith'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_people(
            q='John Smith',
            type='judge'
        )
        
        self.client.get.assert_called_once_with(
            '/people/',
            params={
                'q': 'John Smith',
                'type': 'judge'
            }
        )
        assert result == mock_response
    
    def test_search_recap(self):
        """Test searching RECAP documents."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'document_type': 'motion'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_recap(
            q='test query',
            court='nyed'
        )
        
        self.client.get.assert_called_once_with(
            '/recap/',
            params={
                'q': 'test query',
                'court': 'nyed'
            }
        )
        assert result == mock_response
    
    def test_search_oral_arguments(self):
        """Test searching oral arguments."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'docket': 1}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_oral_arguments(
            docket=1,
            date_argued_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            '/oral-arguments/',
            params={
                'docket': 1,
                'date_argued_min': '2020-01-01'
            }
        )
        assert result == mock_response
    
    def test_search_opinions_clusters(self):
        """Test searching opinion clusters."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'case_name': 'Test Case'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_opinions_clusters(
            q='test query',
            court='scotus'
        )
        
        self.client.get.assert_called_once_with(
            '/opinion-clusters/',
            params={
                'q': 'test query',
                'court': 'scotus'
            }
        )
        assert result == mock_response
    
    def test_error_handling(self):
        """Test error handling in search methods."""
        self.client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.search_api.search_opinions(q='test')
    
    def test_empty_results(self):
        """Test handling of empty search results."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_opinions(q='nonexistent')
        
        assert result['count'] == 0
        assert result['results'] == []
    
    def test_pagination(self):
        """Test pagination in search results."""
        mock_response = {
            'count': 100,
            'next': '/api/rest/v4/opinions/?page=2',
            'previous': None,
            'results': [{'id': 1, 'case_name': 'Test Case'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.search_api.search_opinions(q='test', page=1)
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={'q': 'test', 'page': 1}
        )
        assert result['count'] == 100
        assert result['next'] is not None 