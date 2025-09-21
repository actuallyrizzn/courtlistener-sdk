"""
Comprehensive tests for pagination utilities.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.utils.pagination import Paginator, PageIterator, paginate_results
from courtlistener.exceptions import CourtListenerError


class TestPaginatorComprehensive:
    """Test cases for Paginator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test/endpoint"
        self.params = {"param1": "value1"}

    def test_init_with_params(self):
        """Test initialization with parameters."""
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        
        assert paginator.client == self.mock_client
        assert paginator.endpoint == self.endpoint
        assert paginator.params == self.params
        assert paginator.cursor is None
        assert paginator.has_more is True

    def test_init_without_params(self):
        """Test initialization without parameters."""
        paginator = Paginator(self.mock_client, self.endpoint)
        
        assert paginator.client == self.mock_client
        assert paginator.endpoint == self.endpoint
        assert paginator.params == {}
        assert paginator.cursor is None
        assert paginator.has_more is True

    def test_iter_single_page(self):
        """Test iteration through single page of results."""
        mock_response = {
            "results": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)
        
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "Item 1"}
        assert results[1] == {"id": 2, "name": "Item 2"}
        self.mock_client._make_request.assert_called_once_with('GET', self.endpoint, params=self.params)

    def test_iter_multiple_pages(self):
        """Test iteration through multiple pages of results."""
        # First page
        mock_response_1 = {
            "results": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "next": "https://api.example.com/test/endpoint?cursor=abc123"
        }
        
        # Second page
        mock_response_2 = {
            "results": [
                {"id": 3, "name": "Item 3"},
                {"id": 4, "name": "Item 4"}
            ],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response_1, mock_response_2]
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)
        
        assert len(results) == 4
        assert results[0] == {"id": 1, "name": "Item 1"}
        assert results[1] == {"id": 2, "name": "Item 2"}
        assert results[2] == {"id": 3, "name": "Item 3"}
        assert results[3] == {"id": 4, "name": "Item 4"}
        
        # Check that both pages were requested
        assert self.mock_client._make_request.call_count == 2
        
        # Check first call
        first_call = self.mock_client._make_request.call_args_list[0]
        assert first_call[0] == ('GET', self.endpoint)
        assert first_call[1]['params'] == self.params
        
        # Check second call with cursor
        second_call = self.mock_client._make_request.call_args_list[1]
        assert second_call[0] == ('GET', self.endpoint)
        assert second_call[1]['params'] == {**self.params, 'cursor': 'abc123'}

    def test_iter_empty_response(self):
        """Test iteration with empty response."""
        self.mock_client._make_request.return_value = None
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)
        
        assert results == []

    def test_iter_no_results_key(self):
        """Test iteration with response missing results key."""
        mock_response = {"data": "some data"}
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)
        
        assert results == []

    def test_iter_empty_results(self):
        """Test iteration with empty results list."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        results = list(paginator)
        
        assert results == []

    def test_fetch_page_with_cursor(self):
        """Test _fetch_page with cursor parameter."""
        mock_response = {"results": [{"id": 1}]}
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        paginator.cursor = "https://api.example.com/test/endpoint?cursor=xyz789&other=param"
        
        result = paginator._fetch_page()
        
        assert result == mock_response
        self.mock_client._make_request.assert_called_once_with(
            'GET', self.endpoint, params={**self.params, 'cursor': 'xyz789'}
        )

    def test_fetch_page_with_cursor_no_other_params(self):
        """Test _fetch_page with cursor but no other parameters in URL."""
        mock_response = {"results": [{"id": 1}]}
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        paginator.cursor = "https://api.example.com/test/endpoint?cursor=xyz789"
        
        result = paginator._fetch_page()
        
        assert result == mock_response
        self.mock_client._make_request.assert_called_once_with(
            'GET', self.endpoint, params={**self.params, 'cursor': 'xyz789'}
        )

    def test_fetch_page_without_cursor(self):
        """Test _fetch_page without cursor."""
        mock_response = {"results": [{"id": 1}]}
        self.mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        
        result = paginator._fetch_page()
        
        assert result == mock_response
        self.mock_client._make_request.assert_called_once_with('GET', self.endpoint, params=self.params)

    def test_fetch_page_exception(self):
        """Test _fetch_page with exception."""
        self.mock_client._make_request.side_effect = Exception("Network error")
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(CourtListenerError, match="Failed to fetch page: Network error"):
            paginator._fetch_page()

    def test_iter_updates_pagination_state(self):
        """Test that iteration updates pagination state correctly."""
        # First page with next cursor
        mock_response_1 = {
            "results": [{"id": 1}],
            "next": "https://api.example.com/test/endpoint?cursor=next123"
        }
        
        # Second page with no next cursor
        mock_response_2 = {
            "results": [{"id": 2}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response_1, mock_response_2]
        
        paginator = Paginator(self.mock_client, self.endpoint, self.params)
        
        # Before iteration
        assert paginator.cursor is None
        assert paginator.has_more is True
        
        # Iterate through all items - this will process both pages
        results = list(paginator)
        
        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}
        
        # After iteration, cursor should be None and has_more should be False
        assert paginator.cursor is None
        assert paginator.has_more is False


class TestPageIteratorComprehensive:
    """Test cases for PageIterator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test/endpoint"
        self.params = {"param1": "value1"}

    def test_init_with_params(self):
        """Test initialization with parameters."""
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        assert iterator.client == self.mock_client
        assert iterator.endpoint == self.endpoint
        assert iterator.params == self.params
        assert iterator.current_page is None
        assert iterator.current_index == 0
        assert iterator.cursor is None
        assert iterator.has_more is True

    def test_init_without_params(self):
        """Test initialization without parameters."""
        iterator = PageIterator(self.mock_client, self.endpoint)
        
        assert iterator.client == self.mock_client
        assert iterator.endpoint == self.endpoint
        assert iterator.params == {}
        assert iterator.current_page is None
        assert iterator.current_index == 0
        assert iterator.cursor is None
        assert iterator.has_more is True

    def test_iter_returns_self(self):
        """Test that __iter__ returns self."""
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        assert iter(iterator) is iterator

    def test_next_single_page(self):
        """Test __next__ with single page of results."""
        mock_response = {
            "results": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        # Get first item
        item1 = next(iterator)
        assert item1 == {"id": 1, "name": "Item 1"}
        assert iterator.current_index == 1
        
        # Get second item
        item2 = next(iterator)
        assert item2 == {"id": 2, "name": "Item 2"}
        assert iterator.current_index == 2
        
        # Should raise StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_next_multiple_pages(self):
        """Test __next__ with multiple pages of results."""
        # First page
        mock_response_1 = {
            "results": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "next": "https://api.example.com/test/endpoint?cursor=abc123"
        }
        
        # Second page
        mock_response_2 = {
            "results": [
                {"id": 3, "name": "Item 3"},
                {"id": 4, "name": "Item 4"}
            ],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response_1, mock_response_2]
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        # Get items from first page
        item1 = next(iterator)
        assert item1 == {"id": 1, "name": "Item 1"}
        
        item2 = next(iterator)
        assert item2 == {"id": 2, "name": "Item 2"}
        
        # Get items from second page
        item3 = next(iterator)
        assert item3 == {"id": 3, "name": "Item 3"}
        
        item4 = next(iterator)
        assert item4 == {"id": 4, "name": "Item 4"}
        
        # Should raise StopIteration
        with pytest.raises(StopIteration):
            next(iterator)

    def test_next_empty_page(self):
        """Test __next__ with empty page."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(StopIteration):
            next(iterator)

    def test_load_next_page_with_cursor(self):
        """Test _load_next_page with cursor parameter."""
        mock_response = {
            "results": [{"id": 1}],
            "next": "https://api.example.com/test/endpoint?cursor=next123"
        }
        self.mock_client._make_request.return_value = mock_response
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        iterator.cursor = "https://api.example.com/test/endpoint?cursor=xyz789&other=param"
        
        iterator._load_next_page()
        
        assert iterator.current_page == mock_response
        assert iterator.current_index == 0
        assert iterator.cursor == "https://api.example.com/test/endpoint?cursor=next123"
        assert iterator.has_more is True
        
        self.mock_client._make_request.assert_called_once_with(
            'GET', self.endpoint, params={**self.params, 'cursor': 'xyz789'}
        )

    def test_load_next_page_without_cursor(self):
        """Test _load_next_page without cursor."""
        mock_response = {
            "results": [{"id": 1}],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        iterator._load_next_page()
        
        assert iterator.current_page == mock_response
        assert iterator.current_index == 0
        assert iterator.cursor is None
        assert iterator.has_more is False
        
        self.mock_client._make_request.assert_called_once_with('GET', self.endpoint, params=self.params)

    def test_load_next_page_exception(self):
        """Test _load_next_page with exception."""
        self.mock_client._make_request.side_effect = Exception("Network error")
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        with pytest.raises(CourtListenerError, match="Failed to load page: Network error"):
            iterator._load_next_page()

    def test_next_updates_state_correctly(self):
        """Test that __next__ updates state correctly."""
        # First page with next cursor
        mock_response_1 = {
            "results": [{"id": 1}, {"id": 2}],
            "next": "https://api.example.com/test/endpoint?cursor=next123"
        }
        
        # Second page with no next cursor
        mock_response_2 = {
            "results": [{"id": 3}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response_1, mock_response_2]
        
        iterator = PageIterator(self.mock_client, self.endpoint, self.params)
        
        # Get first item
        item1 = next(iterator)
        assert item1 == {"id": 1}
        assert iterator.current_index == 1
        assert iterator.has_more is True
        
        # Get second item
        item2 = next(iterator)
        assert item2 == {"id": 2}
        assert iterator.current_index == 2
        assert iterator.has_more is True
        
        # Get third item (should load next page)
        item3 = next(iterator)
        assert item3 == {"id": 3}
        assert iterator.current_index == 1  # Reset for new page
        assert iterator.has_more is False


class TestPaginateResultsFunction:
    """Test cases for paginate_results function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.endpoint = "test/endpoint"
        self.params = {"param1": "value1"}

    def test_paginate_results_single_page(self):
        """Test paginate_results with single page."""
        mock_response = {
            "results": [
                {"id": 1, "name": "Item 1"},
                {"id": 2, "name": "Item 2"}
            ],
            "next": None
        }
        self.mock_client._make_request.return_value = mock_response
        
        results = list(paginate_results(self.mock_client, self.endpoint, self.params))
        
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "Item 1"}
        assert results[1] == {"id": 2, "name": "Item 2"}

    def test_paginate_results_multiple_pages(self):
        """Test paginate_results with multiple pages."""
        # First page
        mock_response_1 = {
            "results": [{"id": 1}],
            "next": "https://api.example.com/test/endpoint?cursor=abc123"
        }
        
        # Second page
        mock_response_2 = {
            "results": [{"id": 2}],
            "next": None
        }
        
        self.mock_client._make_request.side_effect = [mock_response_1, mock_response_2]
        
        results = list(paginate_results(self.mock_client, self.endpoint, self.params))
        
        assert len(results) == 2
        assert results[0] == {"id": 1}
        assert results[1] == {"id": 2}

    def test_paginate_results_without_params(self):
        """Test paginate_results without parameters."""
        mock_response = {"results": [{"id": 1}], "next": None}
        self.mock_client._make_request.return_value = mock_response
        
        results = list(paginate_results(self.mock_client, self.endpoint))
        
        assert len(results) == 1
        assert results[0] == {"id": 1}

    def test_paginate_results_empty(self):
        """Test paginate_results with empty results."""
        mock_response = {"results": [], "next": None}
        self.mock_client._make_request.return_value = mock_response
        
        results = list(paginate_results(self.mock_client, self.endpoint, self.params))
        
        assert results == []

    def test_paginate_results_uses_paginator(self):
        """Test that paginate_results uses Paginator internally."""
        mock_response = {"results": [{"id": 1}], "next": None}
        self.mock_client._make_request.return_value = mock_response
        
        with patch('courtlistener.utils.pagination.Paginator') as mock_paginator_class:
            mock_paginator = Mock()
            mock_paginator_class.return_value = mock_paginator
            mock_paginator.__iter__ = Mock(return_value=iter([{"id": 1}]))
            
            results = list(paginate_results(self.mock_client, self.endpoint, self.params))
            
            mock_paginator_class.assert_called_once_with(self.mock_client, self.endpoint, self.params)
            assert results == [{"id": 1}]


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_paginator_cursor_without_cursor_param(self):
        """Test paginator with cursor URL that doesn't contain cursor parameter."""
        mock_client = Mock()
        paginator = Paginator(mock_client, "test/endpoint")
        paginator.cursor = "https://api.example.com/test/endpoint?other=param"
        
        mock_response = {"results": [{"id": 1}]}
        mock_client._make_request.return_value = mock_response
        
        result = paginator._fetch_page()
        
        assert result == mock_response
        # Should not add cursor parameter since it's not in the URL
        mock_client._make_request.assert_called_once_with('GET', 'test/endpoint', params={})

    def test_page_iterator_cursor_without_cursor_param(self):
        """Test page iterator with cursor URL that doesn't contain cursor parameter."""
        mock_client = Mock()
        iterator = PageIterator(mock_client, "test/endpoint")
        iterator.cursor = "https://api.example.com/test/endpoint?other=param"
        
        mock_response = {"results": [{"id": 1}], "next": None}
        mock_client._make_request.return_value = mock_response
        
        iterator._load_next_page()
        
        assert iterator.current_page == mock_response
        # Should not add cursor parameter since it's not in the URL
        mock_client._make_request.assert_called_once_with('GET', 'test/endpoint', params={})

    def test_paginator_cursor_with_multiple_cursor_params(self):
        """Test paginator with cursor URL containing multiple cursor parameters."""
        mock_client = Mock()
        paginator = Paginator(mock_client, "test/endpoint")
        paginator.cursor = "https://api.example.com/test/endpoint?cursor=first&cursor=second"
        
        mock_response = {"results": [{"id": 1}]}
        mock_client._make_request.return_value = mock_response
        
        result = paginator._fetch_page()
        
        assert result == mock_response
        # Should use the first cursor value
        mock_client._make_request.assert_called_once_with('GET', 'test/endpoint', params={'cursor': 'first'})

    def test_page_iterator_cursor_with_multiple_cursor_params(self):
        """Test page iterator with cursor URL containing multiple cursor parameters."""
        mock_client = Mock()
        iterator = PageIterator(mock_client, "test/endpoint")
        iterator.cursor = "https://api.example.com/test/endpoint?cursor=first&cursor=second"
        
        mock_response = {"results": [{"id": 1}], "next": None}
        mock_client._make_request.return_value = mock_response
        
        iterator._load_next_page()
        
        assert iterator.current_page == mock_response
        # Should use the first cursor value
        mock_client._make_request.assert_called_once_with('GET', 'test/endpoint', params={'cursor': 'first'})

    def test_paginator_response_without_next_key(self):
        """Test paginator with response missing next key."""
        mock_response = {"results": [{"id": 1}]}
        mock_client = Mock()
        mock_client._make_request.return_value = mock_response
        
        paginator = Paginator(mock_client, "test/endpoint")
        results = list(paginator)
        
        assert results == [{"id": 1}]
        assert paginator.cursor is None
        assert paginator.has_more is False

    def test_page_iterator_response_without_next_key(self):
        """Test page iterator with response missing next key."""
        mock_response = {"results": [{"id": 1}]}
        mock_client = Mock()
        mock_client._make_request.return_value = mock_response
        
        iterator = PageIterator(mock_client, "test/endpoint")
        item = next(iterator)
        
        assert item == {"id": 1}
        assert iterator.cursor is None
        assert iterator.has_more is False
