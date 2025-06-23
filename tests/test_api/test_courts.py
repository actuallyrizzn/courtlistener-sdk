import pytest
from unittest.mock import Mock, patch
from courtlistener.api.courts import CourtsAPI
from courtlistener.exceptions import CourtListenerError


class TestCourtsAPI:
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.courts_api = CourtsAPI(self.client)
    
    def test_get_court(self):
        """Test getting a single court."""
        mock_response = {
            'id': 1,
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS',
            'jurisdiction': 'F'
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court(1)
        
        self.client.get.assert_called_once_with('/courts/1/')
        assert result == mock_response
    
    def test_get_court_by_url(self):
        """Test getting a court by URL."""
        mock_response = {
            'id': 1,
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS',
            'url': 'scotus'
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court_by_url('scotus')
        
        self.client.get.assert_called_once_with('/courts/scotus/')
        assert result == mock_response
    
    def test_list_courts(self):
        """Test listing courts."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'name': 'Supreme Court of the United States'},
                {'id': 2, 'name': 'Court of Appeals for the First Circuit'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.list_courts(
            jurisdiction='F',
            page=1
        )
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={
                'jurisdiction': 'F',
                'page': 1
            }
        )
        assert result == mock_response
    
    def test_list_courts_with_filters(self):
        """Test listing courts with filters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        filters = {
            'jurisdiction': 'S',
            'start_date_min': '1900-01-01'
        }
        
        result = self.courts_api.list_courts(filters=filters)
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params=filters
        )
        assert result == mock_response
    
    def test_get_federal_courts(self):
        """Test getting federal courts."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'name': 'Supreme Court of the United States'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_federal_courts()
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'jurisdiction': 'F'}
        )
        assert result == mock_response
    
    def test_get_state_courts(self):
        """Test getting state courts."""
        mock_response = {
            'count': 1,
            'results': [{'id': 2, 'name': 'California Supreme Court'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_state_courts()
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'jurisdiction': 'S'}
        )
        assert result == mock_response
    
    def test_get_territorial_courts(self):
        """Test getting territorial courts."""
        mock_response = {
            'count': 1,
            'results': [{'id': 3, 'name': 'Puerto Rico Supreme Court'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_territorial_courts()
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'jurisdiction': 'T'}
        )
        assert result == mock_response
    
    def test_get_active_courts(self):
        """Test getting active courts."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'name': 'Supreme Court of the United States'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_active_courts()
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'end_date': None}
        )
        assert result == mock_response
    
    def test_get_defunct_courts(self):
        """Test getting defunct courts."""
        mock_response = {
            'count': 1,
            'results': [{'id': 4, 'name': 'Defunct Court'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_defunct_courts()
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'end_date__isnull': False}
        )
        assert result == mock_response
    
    def test_get_court_opinions(self):
        """Test getting opinions for a court."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'type': '010combined'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court_opinions(1)
        
        self.client.get.assert_called_once_with('/courts/1/opinions/')
        assert result == mock_response
    
    def test_get_court_opinions_with_params(self):
        """Test getting court opinions with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court_opinions(
            1,
            type='010combined',
            date_filed_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            '/courts/1/opinions/',
            params={
                'type': '010combined',
                'date_filed_min': '2020-01-01'
            }
        )
        assert result == mock_response
    
    def test_get_court_dockets(self):
        """Test getting dockets for a court."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'docket_number': '21-123'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court_dockets(1)
        
        self.client.get.assert_called_once_with('/courts/1/dockets/')
        assert result == mock_response
    
    def test_error_handling(self):
        """Test error handling in court methods."""
        self.client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.courts_api.get_court(1)
    
    def test_not_found_handling(self):
        """Test handling of not found courts."""
        self.client.get.side_effect = CourtListenerError("Not found", status_code=404)
        
        with pytest.raises(CourtListenerError) as exc_info:
            self.courts_api.get_court(999)
        
        assert exc_info.value.status_code == 404
    
    def test_empty_court_opinions(self):
        """Test handling of empty court opinions."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.courts_api.get_court_opinions(1)
        
        assert result['count'] == 0
        assert result['results'] == []
    
    def test_pagination_in_courts(self):
        """Test pagination in courts."""
        mock_response = {
            'count': 50,
            'next': '/api/rest/v4/courts/?page=2',
            'previous': None,
            'results': [{'id': 1, 'name': 'Test Court'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.courts_api.list_courts(page=1)
        
        self.client.get.assert_called_once_with(
            '/courts/',
            params={'page': 1}
        )
        assert result['count'] == 50
        assert result['next'] is not None
    
    def test_jurisdiction_types(self):
        """Test filtering by jurisdiction types."""
        mock_response = {'count': 1, 'results': [{'id': 1, 'jurisdiction': 'F'}]}
        self.client.get.return_value = mock_response
        
        # Test federal jurisdiction
        result = self.courts_api.list_courts(jurisdiction='F')
        self.client.get.assert_called_with('/courts/', params={'jurisdiction': 'F'})
        
        # Test state jurisdiction
        result = self.courts_api.list_courts(jurisdiction='S')
        self.client.get.assert_called_with('/courts/', params={'jurisdiction': 'S'})
        
        # Test territorial jurisdiction
        result = self.courts_api.list_courts(jurisdiction='T')
        self.client.get.assert_called_with('/courts/', params={'jurisdiction': 'T'}) 