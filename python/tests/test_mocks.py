import pytest
from unittest.mock import Mock, patch, MagicMock
from courtlistener import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError, AuthenticationError, RateLimitError, 
    ValidationError, APIError, NotFoundError
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
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.search.search_opinions(q='test')
            
            # search_opinions returns Dict[str, Any]
            assert isinstance(result, dict)
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
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.dockets.get_docket(1)
            
            # get_docket returns a Docket model object
            assert hasattr(result, 'id')
            assert result.id == 1
            assert result.docket_number == '21-123'
    
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
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.opinions.get_opinion(1)
            
            # get_opinion returns an Opinion model object
            assert hasattr(result, 'id')
            assert result.id == 1
            assert result.type == '010combined'
    
    def test_mock_successful_court_response(self):
        """Test mocking a successful court response."""
        mock_response = {
            'id': 'scotus',
            'name': 'Supreme Court of the United States',
            'short_name': 'SCOTUS',
            'full_name': 'Supreme Court of the United States',
            'jurisdiction': 'F',
            'url': 'scotus'
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.courts.get_court('scotus')
            
            # get_court returns a Court model object
            assert hasattr(result, 'id')
            assert result.id == 'scotus'
            # The Court model's name property returns short_name from API
            assert result.name == 'SCOTUS'
            # Check full_name if available
            if hasattr(result, 'full_name'):
                assert result.full_name == 'Supreme Court of the United States'


class TestMockErrorResponses:
    """Test mocking error API responses."""
    
    def test_mock_authentication_error(self):
        """Test mocking authentication error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = AuthenticationError('Invalid API token')
            
            with pytest.raises(AuthenticationError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Invalid API token' in str(exc_info.value)
    
    def test_mock_rate_limit_error(self):
        """Test mocking rate limit error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = RateLimitError('Rate limit exceeded')
            
            with pytest.raises(RateLimitError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Rate limit exceeded' in str(exc_info.value)
    
    def test_mock_404_error(self):
        """Test mocking 404 Not Found error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = NotFoundError('Not found')
            
            with pytest.raises(NotFoundError) as exc_info:
                client.dockets.get_docket(999999)
            assert exc_info.value.status_code == 404
    
    def test_mock_400_error(self):
        """Test mocking 400 Bad Request error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = APIError('Bad request', status_code=400)
            
            with pytest.raises(APIError) as exc_info:
                client.search.search_opinions(q='')
            assert exc_info.value.status_code == 400
    
    def test_mock_500_error(self):
        """Test mocking 500 Server Error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = APIError('Internal server error', status_code=500)
            
            with pytest.raises(APIError) as exc_info:
                client.search.search_opinions(q='test')
            assert exc_info.value.status_code == 500
    
    def test_mock_validation_error(self):
        """Test mocking validation error response."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = ValidationError('Invalid date format')
            
            with pytest.raises(ValidationError) as exc_info:
                client.search.search_opinions(q='test', date_filed_min='invalid-date')
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
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.opinions.list_opinions(page=1)
            
            # list_opinions returns List[Opinion], not dict
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].id == 1
    
    def test_mock_pagination_with_previous_page(self):
        """Test mocking pagination with previous page."""
        mock_response = {
            'count': 100,
            'next': None,
            'previous': '/api/rest/v4/opinions/?page=1',
            'results': [{'id': 2, 'case_name': 'Test Case 2'}]
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.opinions.list_opinions(page=2)
            
            # list_opinions returns List[Opinion], not dict
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0].id == 2
    
    def test_mock_pagination_middle_page(self):
        """Test mocking pagination for middle page."""
        mock_response = {
            'count': 100,
            'next': '/api/rest/v4/opinions/?page=3',
            'previous': '/api/rest/v4/opinions/?page=1',
            'results': [{'id': 2, 'case_name': 'Test Case 2'}]
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.opinions.list_opinions(page=2)
            
            # list_opinions returns List[Opinion], not dict
            assert isinstance(result, list)
            assert len(result) == 1
    
    def test_mock_pagination_last_page(self):
        """Test mocking pagination for last page."""
        mock_response = {
            'count': 100,
            'next': None,
            'previous': '/api/rest/v4/opinions/?page=9',
            'results': [{'id': 100, 'case_name': 'Test Case 100'}]
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.opinions.list_opinions(page=10)
            
            # list_opinions returns List[Opinion], not dict
            assert isinstance(result, list)
            assert len(result) == 1
    
    def test_mock_empty_pagination(self):
        """Test mocking empty pagination results."""
        mock_response = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.return_value = mock_response
            result = client.search.search_opinions(q='nonexistent')
            
            # search_opinions returns Dict[str, Any]
            assert isinstance(result, dict)
            assert result.get('count') == 0
            assert result.get('next') is None
            assert result.get('previous') is None
            assert len(result.get('results', [])) == 0


class TestMockRateLimiting:
    """Test mocking rate limiting scenarios."""
    
    def test_mock_rate_limit_exceeded(self):
        """Test mocking rate limit exceeded."""
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = RateLimitError('Rate limit exceeded')
            
            with pytest.raises(RateLimitError):
                client.search.search_opinions(q='test')
    
    def test_mock_rate_limit_with_retry(self):
        """Test mocking rate limit with retry logic."""
        # Mock at the session level to test actual retry behavior
        with patch('requests.Session.request') as mock_session:
            # First call returns 429, second succeeds
            mock_response_429 = Mock()
            mock_response_429.status_code = 429
            mock_response_429.headers = {'Retry-After': '1'}
            mock_response_429.json.return_value = {'detail': 'Rate limit exceeded'}
            
            mock_response_200 = Mock()
            mock_response_200.status_code = 200
            mock_response_200.json.return_value = {'results': [], 'count': 0}
            
            mock_session.side_effect = [mock_response_429, mock_response_200]
            client = CourtListenerClient(api_token='dummy', max_retries=3)
            
            # Should retry and eventually succeed
            result = client.search.search_opinions(q='test')
            assert isinstance(result, dict) and 'results' in result
    
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
            client = CourtListenerClient(api_token='dummy')
            
            with pytest.raises(RateLimitError) as exc_info:
                client.search.search_opinions(q='test')
            assert 'Rate limit exceeded' in str(exc_info.value)
    
    def test_mock_rate_limit_backoff(self):
        """Test mocking rate limit with exponential backoff."""
        # Mock at the session level to test actual retry behavior
        with patch('requests.Session.request') as mock_session:
            # Multiple 429 responses before success
            mock_response_429 = Mock()
            mock_response_429.status_code = 429
            mock_response_429.headers = {'Retry-After': '1'}
            mock_response_429.json.return_value = {'detail': 'Rate limit exceeded'}
            
            mock_response_200 = Mock()
            mock_response_200.status_code = 200
            mock_response_200.json.return_value = {'results': [], 'count': 0}
            
            mock_session.side_effect = [mock_response_429, mock_response_429, mock_response_429, mock_response_200]
            client = CourtListenerClient(api_token='dummy', max_retries=3)
            
            # Should retry multiple times and eventually succeed
            result = client.search.search_opinions(q='test')
            assert isinstance(result, dict) and 'results' in result


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
            '/clusters/1/': {
                'id': 1,
                'case_name': 'Test Case',
                'court': None,
                'date_filed': None
            },
            '/opinion-clusters/1/opinions/': {
                'count': 1,
                'results': [{'id': 1, 'type': '010combined'}]
            }
        }
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            def mock_request_side_effect(method, endpoint, **kwargs):
                # Return appropriate mock response based on endpoint
                params = kwargs.get('params', {})
                if endpoint == '/opinions/1/':
                    return mock_responses['/opinions/1/']
                elif endpoint == '/clusters/1/':
                    return mock_responses['/clusters/1/']
                elif endpoint == '/opinions/' and params.get('cluster') == 1:
                    return mock_responses['/opinion-clusters/1/opinions/']
                elif endpoint == '/search/':
                    return mock_responses['/opinions/']
                else:
                    return mock_responses['/opinions/']
            
            mock_request.side_effect = mock_request_side_effect
            
            # Execute workflow
            opinions = client.search.search_opinions(q='test')
            opinion_detail = client.opinions.get_opinion(1)
            cluster = client.clusters.get_cluster(1)
            # Get opinions in cluster using the opinions API
            cluster_opinions = client.opinions.get_opinions_in_cluster(1)
            
            # Verify results
            assert isinstance(opinions, dict) and opinions.get('count') == 1
            assert hasattr(opinion_detail, 'id') and opinion_detail.id == 1
            assert hasattr(cluster, 'id') and cluster.id == 1
            # cluster_opinions is a list of Opinion objects
            assert isinstance(cluster_opinions, list) and len(cluster_opinions) == 1
    
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
        
        client = CourtListenerClient(api_token='dummy')
        with patch.object(client.transport, '_make_request') as mock_request:
            mock_request.side_effect = [r for r in mock_responses]
            
            # Test first page
            page1 = client.opinions.list_opinions(page=1)
            assert isinstance(page1, list)
            assert len(page1) == 100
            
            # Test middle page
            page5 = client.opinions.list_opinions(page=5)
            assert isinstance(page5, list)
            assert len(page5) == 100
            
            # Test last page
            page10 = client.opinions.list_opinions(page=10)
            assert isinstance(page10, list)
            assert len(page10) == 100 
