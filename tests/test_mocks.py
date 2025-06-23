import pytest
from unittest.mock import Mock, patch, MagicMock
from courtlistener.client import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError, AuthenticationError, RateLimitError, 
    ValidationError, APIError
)


class TestMockSuccessfulResponses:
    """Test mocking successful API responses."""
    
    def test_mock_successful_search_response(self):
        """Test mocking a successful search response."""
        mock_response = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {'id': 1, 'case_name': 'Test Case 1'},
                {'id': 2, 'case_name': 'Test Case 2'}
            ]
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.search.search_opinions(q='test')
            
            assert result == mock_response
            assert result['count'] == 2
            assert len(result['results']) == 2
            assert result['results'][0]['case_name'] == 'Test Case 1'
    
    def test_mock_successful_docket_response(self):
        """Test mocking a successful docket response."""
        mock_response = {
            'id': 1,
            'docket_number': '21-123',
            'case_name': 'Smith v. Jones',
            'court': 1,
            'date_filed': '2020-01-01T00:00:00Z'
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.dockets.get_docket(1)
            
            assert result == mock_response
            assert result['id'] == 1
            assert result['docket_number'] == '21-123'
    
    def test_mock_successful_opinion_response(self):
        """Test mocking a successful opinion response."""
        mock_response = {
            'id': 1,
            'cluster': 1,
            'author': 1,
            'type': '010combined',
            'type_name': 'Majority Opinion',
            'html': '<p>This is the opinion text</p>'
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.opinions.get_opinion(1)
            
            assert result == mock_response
            assert result['id'] == 1
            assert result['type'] == '010combined'
    
    def test_mock_successful_court_response(self):
        """Test mocking a successful court response."""
        mock_response = {
            'id': 1,
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS',
            'jurisdiction': 'F',
            'url': 'scotus'
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.courts.get_court(1)
            
            assert result == mock_response
            assert result['name'] == 'Supreme Court of the United States'
            assert result['short_name'] == 'SCOTUS'


class TestMockErrorResponses:
    """Test mocking error API responses."""
    
    def test_mock_authentication_error(self):
        """Test mocking authentication error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = AuthenticationError('Invalid token')
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(AuthenticationError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Invalid token' in str(exc_info.value)
    
    def test_mock_rate_limit_error(self):
        """Test mocking rate limit error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = RateLimitError('Rate limit exceeded')
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(RateLimitError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Rate limit exceeded' in str(exc_info.value)
    
    def test_mock_404_error(self):
        """Test mocking 404 Not Found error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = CourtListenerError('Not found', status_code=404)
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(CourtListenerError) as exc_info:
                client.dockets.get_docket(999999)
            assert exc_info.value.status_code == 404
    
    def test_mock_400_error(self):
        """Test mocking 400 Bad Request error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = CourtListenerError('Bad request', status_code=400)
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(CourtListenerError) as exc_info:
                client.search.search_opinions(q='')
            assert exc_info.value.status_code == 400
    
    def test_mock_500_error(self):
        """Test mocking 500 Server Error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = APIError('Internal server error', status_code=500)
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(APIError) as exc_info:
                client.search.search_opinions(q='test')
            assert exc_info.value.status_code == 500
    
    def test_mock_validation_error(self):
        """Test mocking validation error response."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = ValidationError('Invalid date format')
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(ValidationError) as exc_info:
                client.search.search_opinions(date_filed_min='invalid-date')
            assert 'Invalid date format' in str(exc_info.value)


class TestMockPaginationScenarios:
    """Test mocking pagination scenarios."""
    
    def test_mock_pagination_with_next_page(self):
        """Test mocking pagination with next page."""
        mock_response = {
            'count': 100,
            'next': '/api/rest/v4/opinions/?page=2',
            'previous': None,
            'results': [{'id': 1, 'case_name': 'Test Case 1'}]
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.opinions.list_opinions(page=1)
            
            assert result['count'] == 100
            assert result['next'] == '/api/rest/v4/opinions/?page=2'
            assert result['previous'] is None
            assert len(result['results']) == 1
    
    def test_mock_pagination_with_previous_page(self):
        """Test mocking pagination with previous page."""
        mock_response = {
            'count': 100,
            'next': None,
            'previous': '/api/rest/v4/opinions/?page=1',
            'results': [{'id': 2, 'case_name': 'Test Case 2'}]
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.opinions.list_opinions(page=2)
            
            assert result['count'] == 100
            assert result['next'] is None
            assert result['previous'] == '/api/rest/v4/opinions/?page=1'
            assert len(result['results']) == 1
    
    def test_mock_pagination_middle_page(self):
        """Test mocking pagination for middle page."""
        mock_response = {
            'count': 100,
            'next': '/api/rest/v4/opinions/?page=3',
            'previous': '/api/rest/v4/opinions/?page=1',
            'results': [{'id': 2, 'case_name': 'Test Case 2'}]
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.opinions.list_opinions(page=2)
            
            assert result['count'] == 100
            assert result['next'] == '/api/rest/v4/opinions/?page=3'
            assert result['previous'] == '/api/rest/v4/opinions/?page=1'
    
    def test_mock_pagination_last_page(self):
        """Test mocking pagination for last page."""
        mock_response = {
            'count': 100,
            'next': None,
            'previous': '/api/rest/v4/opinions/?page=9',
            'results': [{'id': 100, 'case_name': 'Test Case 100'}]
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.opinions.list_opinions(page=10)
            
            assert result['count'] == 100
            assert result['next'] is None
            assert result['previous'] == '/api/rest/v4/opinions/?page=9'
    
    def test_mock_empty_pagination(self):
        """Test mocking empty pagination results."""
        mock_response = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            result = client.search.search_opinions(q='nonexistent')
            
            assert result['count'] == 0
            assert result['next'] is None
            assert result['previous'] is None
            assert len(result['results']) == 0


class TestMockRateLimiting:
    """Test mocking rate limiting scenarios."""
    
    def test_mock_rate_limit_exceeded(self):
        """Test mocking rate limit exceeded."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = RateLimitError('Rate limit exceeded')
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(RateLimitError):
                client.search.search_opinions(q='test')
    
    def test_mock_rate_limit_with_retry(self):
        """Test mocking rate limit with retry logic."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            # First call fails with rate limit, second succeeds
            mock_request.side_effect = [
                RateLimitError('Rate limit exceeded'),
                {'results': [], 'count': 0}
            ]
            client = CourtListenerClient(api_key='dummy')
            
            # Should retry and eventually succeed
            result = client.search.search_opinions(q='test')
            assert 'results' in result
    
    def test_mock_rate_limit_headers(self):
        """Test mocking rate limit with headers."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {
            'X-RateLimit-Limit': '100',
            'X-RateLimit-Remaining': '0',
            'X-RateLimit-Reset': '1640995200'
        }
        mock_response.json.return_value = {'detail': 'Rate limit exceeded'}
        
        with patch('requests.Session.request') as mock_request:
            mock_request.return_value = mock_response
            client = CourtListenerClient(api_key='dummy')
            
            with pytest.raises(RateLimitError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Rate limit exceeded' in str(exc_info.value)
    
    def test_mock_rate_limit_backoff(self):
        """Test mocking rate limit with exponential backoff."""
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            # Multiple rate limit errors before success
            mock_request.side_effect = [
                RateLimitError('Rate limit exceeded'),
                RateLimitError('Rate limit exceeded'),
                RateLimitError('Rate limit exceeded'),
                {'results': [], 'count': 0}
            ]
            client = CourtListenerClient(api_key='dummy')
            
            # Should retry multiple times and eventually succeed
            result = client.search.search_opinions(q='test')
            assert 'results' in result


class TestMockComplexScenarios:
    """Test mocking complex scenarios."""
    
    def test_mock_multi_endpoint_workflow(self):
        """Test mocking a complex multi-endpoint workflow."""
        # Mock responses for a complete workflow
        mock_responses = {
            '/opinions/': {
                'count': 1,
                'results': [{'id': 1, 'cluster': 1}]
            },
            '/opinions/1/': {
                'id': 1,
                'cluster': 1,
                'type': '010combined'
            },
            '/opinion-clusters/1/': {
                'id': 1,
                'case_name': 'Test Case'
            },
            '/opinion-clusters/1/opinions/': {
                'count': 1,
                'results': [{'id': 1, 'type': '010combined'}]
            }
        }
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            def mock_request_side_effect(endpoint, **kwargs):
                # Return appropriate mock response based on endpoint
                if 'opinions/' in endpoint and not endpoint.endswith('/opinions/'):
                    return mock_responses['/opinions/1/']
                elif 'opinion-clusters/' in endpoint and not endpoint.endswith('/opinions/'):
                    return mock_responses['/opinion-clusters/1/']
                elif 'opinion-clusters/' in endpoint and endpoint.endswith('/opinions/'):
                    return mock_responses['/opinion-clusters/1/opinions/']
                else:
                    return mock_responses['/opinions/']
            
            mock_request.side_effect = mock_request_side_effect
            client = CourtListenerClient(api_key='dummy')
            
            # Execute workflow
            opinions = client.search.search_opinions(q='test')
            opinion_detail = client.opinions.get_opinion(1)
            cluster = client.opinion_clusters.get_opinion_cluster(1)
            cluster_opinions = client.opinion_clusters.get_opinions_in_cluster(1)
            
            # Verify results
            assert opinions['count'] == 1
            assert opinion_detail['id'] == 1
            assert cluster['id'] == 1
            assert cluster_opinions['count'] == 1
    
    def test_mock_large_dataset_pagination(self):
        """Test mocking large dataset pagination."""
        # Create mock responses for 10 pages
        mock_responses = []
        for page in range(1, 11):
            mock_responses.append({
                'count': 1000,
                'next': f'/api/rest/v4/opinions/?page={page + 1}' if page < 10 else None,
                'previous': f'/api/rest/v4/opinions/?page={page - 1}' if page > 1 else None,
                'results': [{'id': i, 'case_name': f'Test Case {i}'} for i in range((page-1)*100+1, page*100+1)]
            })
        
        with patch('courtlistener.client.CourtListenerClient._request') as mock_request:
            mock_request.side_effect = mock_responses
            client = CourtListenerClient(api_key='dummy')
            
            # Test first page
            page1 = client.opinions.list_opinions(page=1)
            assert page1['count'] == 1000
            assert page1['next'] == '/api/rest/v4/opinions/?page=2'
            assert page1['previous'] is None
            assert len(page1['results']) == 100
            
            # Test middle page
            page5 = client.opinions.list_opinions(page=5)
            assert page5['next'] == '/api/rest/v4/opinions/?page=6'
            assert page5['previous'] == '/api/rest/v4/opinions/?page=4'
            
            # Test last page
            page10 = client.opinions.list_opinions(page=10)
            assert page10['next'] is None
            assert page10['previous'] == '/api/rest/v4/opinions/?page=9' 