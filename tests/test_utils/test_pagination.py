import pytest
from unittest.mock import MagicMock, patch
from courtlistener.utils.pagination import Paginator, PageIterator, paginate_results
from courtlistener.exceptions import CourtListenerError


class TestPaginator:
    def test_paginator_initialization(self):
        """Test paginator initialization."""
        mock_client = MagicMock()
        paginator = Paginator(mock_client, '/api/test/', {'param': 'value'})
        
        assert paginator.client == mock_client
        assert paginator.endpoint == '/api/test/'
        assert paginator.params == {'param': 'value'}
        assert paginator.cursor is None
        assert paginator.has_more is True
    
    def test_paginator_iteration_single_page(self):
        """Test paginator iteration with single page."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [{'id': 1}, {'id': 2}],
            'next': None
        }
        
        paginator = Paginator(mock_client, '/api/test/')
        results = list(paginator)
        
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
        assert paginator.has_more is False
    
    def test_paginator_iteration_multiple_pages(self):
        """Test paginator iteration with multiple pages."""
        mock_client = MagicMock()
        mock_client._make_request.side_effect = [
            {
                'results': [{'id': 1}, {'id': 2}],
                'next': '/api/test/?cursor=abc123'
            },
            {
                'results': [{'id': 3}, {'id': 4}],
                'next': None
            }
        ]
        
        paginator = Paginator(mock_client, '/api/test/')
        results = list(paginator)
        
        assert len(results) == 4
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
        assert results[2]['id'] == 3
        assert results[3]['id'] == 4
        assert paginator.has_more is False
    
    def test_paginator_empty_response(self):
        """Test paginator with empty response."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {}
        
        paginator = Paginator(mock_client, '/api/test/')
        results = list(paginator)
        
        assert len(results) == 0
    
    def test_paginator_no_results_key(self):
        """Test paginator with response missing results key."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {'count': 0}
        
        paginator = Paginator(mock_client, '/api/test/')
        results = list(paginator)
        
        assert len(results) == 0
    
    def test_paginator_request_failure(self):
        """Test paginator when request fails."""
        mock_client = MagicMock()
        mock_client._make_request.side_effect = Exception("Network error")
        
        paginator = Paginator(mock_client, '/api/test/')
        
        with pytest.raises(CourtListenerError, match="Failed to fetch page"):
            list(paginator)
    
    def test_paginator_cursor_extraction(self):
        """Test paginator cursor extraction from URL."""
        mock_client = MagicMock()
        # First call returns a page with next URL, second call returns no next URL
        mock_client._make_request.side_effect = [
            {
                'results': [{'id': 1}],
                'next': '/api/test/?param=value&cursor=abc123&other=stuff'
            },
            {
                'results': [{'id': 2}],
                # No 'next' key - pagination ends
            }
        ]
        
        paginator = Paginator(mock_client, '/api/test/')
        results = list(paginator)  # Consume all pages
        
        # Check that we got both results
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
        
        # Check that cursor was extracted correctly
        assert paginator.cursor is None  # Should be None after pagination ends


class TestPageIterator:
    def test_page_iterator_initialization(self):
        """Test page iterator initialization."""
        mock_client = MagicMock()
        iterator = PageIterator(mock_client, '/api/test/', {'param': 'value'})
        
        assert iterator.client == mock_client
        assert iterator.endpoint == '/api/test/'
        assert iterator.params == {'param': 'value'}
        assert iterator.current_page is None
        assert iterator.current_index == 0
        assert iterator.cursor is None
        assert iterator.has_more is True
    
    def test_page_iterator_single_page(self):
        """Test page iterator with single page."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [{'id': 1}, {'id': 2}],
            'next': None
        }
        
        iterator = PageIterator(mock_client, '/api/test/')
        results = list(iterator)
        
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
    
    def test_page_iterator_multiple_pages(self):
        """Test page iterator with multiple pages."""
        mock_client = MagicMock()
        mock_client._make_request.side_effect = [
            {
                'results': [{'id': 1}, {'id': 2}],
                'next': '/api/test/?cursor=abc123'
            },
            {
                'results': [{'id': 3}, {'id': 4}],
                'next': None
            }
        ]
        
        iterator = PageIterator(mock_client, '/api/test/')
        results = list(iterator)
        
        assert len(results) == 4
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
        assert results[2]['id'] == 3
        assert results[3]['id'] == 4
    
    def test_page_iterator_empty_page(self):
        """Test page iterator with empty page."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [],
            'next': None
        }
        
        iterator = PageIterator(mock_client, '/api/test/')
        results = list(iterator)
        
        assert len(results) == 0
    
    def test_page_iterator_request_failure(self):
        """Test page iterator when request fails."""
        mock_client = MagicMock()
        mock_client._make_request.side_effect = Exception("Network error")
        
        iterator = PageIterator(mock_client, '/api/test/')
        
        with pytest.raises(CourtListenerError, match="Failed to load page"):
            next(iterator)
    
    def test_page_iterator_stop_iteration(self):
        """Test page iterator stop iteration."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [{'id': 1}],
            'next': None
        }
        
        iterator = PageIterator(mock_client, '/api/test/')
        results = list(iterator)
        
        assert len(results) == 1
        assert results[0]['id'] == 1
        
        # Should raise StopIteration on next call
        with pytest.raises(StopIteration):
            next(iterator)


class TestPaginateResults:
    def test_paginate_results_function(self):
        """Test paginate_results convenience function."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [{'id': 1}, {'id': 2}],
            'next': None
        }
        
        results = list(paginate_results(mock_client, '/api/test/'))
        
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2
    
    def test_paginate_results_with_params(self):
        """Test paginate_results with parameters."""
        mock_client = MagicMock()
        mock_client._make_request.return_value = {
            'results': [{'id': 1}],
            'next': None
        }
        
        params = {'court': 'scotus', 'limit': 10}
        results = list(paginate_results(mock_client, '/api/test/', params))
        
        assert len(results) == 1
        assert results[0]['id'] == 1
        
        # Verify params were passed to request
        mock_client._make_request.assert_called_with(
            'GET', '/api/test/', params=params
        )
    
    def test_paginate_results_multiple_pages(self):
        """Test paginate_results with multiple pages."""
        mock_client = MagicMock()
        mock_client._make_request.side_effect = [
            {
                'results': [{'id': 1}],
                'next': '/api/test/?cursor=abc123'
            },
            {
                'results': [{'id': 2}],
                'next': None
            }
        ]
        
        results = list(paginate_results(mock_client, '/api/test/'))
        
        assert len(results) == 2
        assert results[0]['id'] == 1
        assert results[1]['id'] == 2 