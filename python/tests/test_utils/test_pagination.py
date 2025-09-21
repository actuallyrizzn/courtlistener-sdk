"""
Comprehensive tests for the pagination utility module.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.utils.pagination import Paginator, PageIterator, paginate_results
from courtlistener.exceptions import CourtListenerError


class TestPaginator:
    """Test cases for Paginator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test-endpoint"
        self.params = {"page": 1}

    def test_paginator_init(self):
        """Test Paginator initialization."""
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        assert paginator.client == self.mock_client
        assert paginator.endpoint == self.endpoint
        assert paginator.params == self.params
        assert paginator.cursor is None
        assert paginator.has_more is True

    def test_paginator_init_no_params(self):
        """Test Paginator initialization with no params."""
        paginator = Paginator(self.mock_client, self.endpoint)
        assert paginator.params == {}

    def test_paginator_iteration_single_page(self):
        """Test paginator iteration with single page."""
        mock_response = {
            "results": [{"id": 1}, {"id": 2}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}
        assert paginator.has_more is False

    def test_paginator_iteration_multiple_pages(self):
        """Test paginator iteration with multiple pages."""
        # First page
        mock_response1 = {
            "results": [{"id": 1}],
            "next": "http://api.test/endpoint?cursor=abc123"
        }
        # Second page
        mock_response2 = {
            "results": [{"id": 2}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response1, mock_response2]

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}
        assert paginator.has_more is False

    def test_paginator_iteration_empty_response(self):
        """Test paginator iteration with empty response."""
        mock_response = {}
        self.mock_client._make_request.return_value = mock_response

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)

        assert len(results) == 0

    def test_paginator_iteration_no_results_key(self):
        """Test paginator iteration with response missing results key."""
        mock_response = {"count": 0}
        self.mock_client._make_request.return_value = mock_response

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)

        assert len(results) == 0

    def test_paginator_iteration_with_cursor(self):
        """Test paginator iteration with cursor parameter."""
        mock_response = {
            "results": [{"id": 1}],
            "next": "http://api.test/endpoint?cursor=xyz789"
        }
        self.mock_client._make_request.return_value = mock_response

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        list(paginator)  # Consume the iterator

        # Check that cursor was extracted and added to params
        call_args = self.mock_client._make_request.call_args
        assert call_args[0] == ('GET', self.endpoint)
        assert 'cursor' in call_args[1]['params']

    def test_paginator_fetch_page_error(self):
        """Test paginator error handling in _fetch_page."""
        self.mock_client._make_request.side_effect = Exception("Network error")

        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(CourtListenerError, match="Failed to fetch page"):
            list(paginator)


class TestPageIterator:
    """Test cases for PageIterator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test-endpoint"
        self.params = {"page": 1}

    def test_page_iterator_init(self):
        """Test PageIterator initialization."""
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        assert iterator.client == self.mock_client
        assert iterator.endpoint == self.endpoint
        assert iterator.params == self.params
        assert iterator.current_page is None
        assert iterator.current_index == 0
        assert iterator.cursor is None
        assert iterator.has_more is True

    def test_page_iterator_init_no_params(self):
        """Test PageIterator initialization with no params."""
        iterator = PageIterator(self.mock_client, self.endpoint)
        assert iterator.params == {}

    def test_page_iterator_iteration_single_page(self):
        """Test page iterator with single page."""
        mock_response = {
            "results": [{"id": 1}, {"id": 2}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        results = list(iterator)

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}

    def test_page_iterator_iteration_multiple_pages(self):
        """Test page iterator with multiple pages."""
        # First page
        mock_response1 = {
            "results": [{"id": 1}],
            "next": "http://api.test/endpoint?cursor=abc123"
        }
        # Second page
        mock_response2 = {
            "results": [{"id": 2}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response1, mock_response2]

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        results = list(iterator)

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}

    def test_page_iterator_next_single_item(self):
        """Test page iterator next() method with single item."""
        mock_response = {
            "results": [{"id": 1}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        # Test first item
        item = next(iterator)
        assert item == {"id": 1}
        
        # Test StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_page_iterator_next_multiple_items(self):
        """Test page iterator next() method with multiple items."""
        mock_response = {
            "results": [{"id": 1}, {"id": 2}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        # Test first item
        item1 = next(iterator)
        assert item1 == {"id": 1}
        
        # Test second item
        item2 = next(iterator)
        assert item2 == {"id": 2}
        
        # Test StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_page_iterator_load_next_page_error(self):
        """Test page iterator error handling in _load_next_page."""
        self.mock_client._make_request.side_effect = Exception("Network error")

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(CourtListenerError, match="Failed to load page"):
            next(iterator)

    def test_page_iterator_with_cursor(self):
        """Test page iterator with cursor parameter."""
        mock_response = {
            "results": [{"id": 1}],
            "next": "http://api.test/endpoint?cursor=xyz789"
        }
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        list(iterator)  # Consume the iterator

        # Check that cursor was extracted and added to params
        call_args = self.mock_client._make_request.call_args
        assert call_args[0] == ('GET', self.endpoint)
        assert 'cursor' in call_args[1]['params']

    def test_page_iterator_empty_results(self):
        """Test page iterator with empty results."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(StopIteration):
            next(iterator)

    def test_page_iterator_no_results_key(self):
        """Test page iterator with response missing results key."""
        mock_response = {"count": 0, "next": None}
        self.mock_client._make_request.return_value = mock_response

        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(StopIteration):
            next(iterator)


class TestPaginateResults:
    """Test cases for paginate_results function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test-endpoint"
        self.params = {"page": 1}

    def test_paginate_results_basic(self):
        """Test basic paginate_results functionality."""
        mock_response = {
            "results": [{"id": 1}, {"id": 2}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response

        results = list(paginate_results(self.mock_client, self.endpoint, self.params))

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}

    def test_paginate_results_no_params(self):
        """Test paginate_results with no params."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response

        results = list(paginate_results(self.mock_client, self.endpoint))

        assert len(results) == 0

    def test_paginate_results_multiple_pages(self):
        """Test paginate_results with multiple pages."""
        # First page
        mock_response1 = {
            "results": [{"id": 1}],
            "next": "http://api.test/endpoint?cursor=abc123"
        }
        # Second page
        mock_response2 = {
            "results": [{"id": 2}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response1, mock_response2]

        results = list(paginate_results(self.mock_client, self.endpoint, self.params))

        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}

    def test_paginate_results_creates_paginator(self):
        """Test that paginate_results creates a Paginator instance."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response

        with patch('courtlistener.utils.pagination.Paginator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator_class.return_value = mock_paginator
            mock_paginator.__iter__ = Mock(return_value=iter([]))

            list(paginate_results(self.mock_client, self.endpoint, self.params))

            mock_paginator_class.assert_called_once_with(self.mock_client, self.endpoint, self.params)