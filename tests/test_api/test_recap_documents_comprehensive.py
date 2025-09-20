"""
Comprehensive tests for the RECAP Documents API module.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.recap_documents import RecapDocumentsAPI


class TestRecapDocumentsAPI:
    """Test cases for RecapDocumentsAPI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = RecapDocumentsAPI(self.mock_client)

    def test_init(self):
        """Test RecapDocumentsAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.endpoint == "recap-documents/"

    def test_list_no_filters(self):
        """Test list method with no filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list()

        expected_params = {}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_list_with_docket_filter(self):
        """Test list method with docket filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "docket": 123}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(docket=123)

        expected_params = {"docket": 123}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_list_with_docket_entry_filter(self):
        """Test list method with docket_entry filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "docket_entry": 456}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(docket_entry=456)

        expected_params = {"docket_entry": 456}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_list_with_court_filter(self):
        """Test list method with court filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "court": "scotus"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(court="scotus")

        expected_params = {"court": "scotus"}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_list_with_multiple_filters(self):
        """Test list method with multiple filters."""
        mock_response = {"count": 1, "results": [{"id": 1, "docket": 123, "docket_entry": 456, "court": "scotus"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(docket=123, docket_entry=456, court="scotus")

        expected_params = {
            "docket": 123,
            "docket_entry": 456,
            "court": "scotus"
        }
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_list_with_additional_kwargs(self):
        """Test list method with additional kwargs."""
        mock_response = {"count": 1, "results": [{"id": 1, "docket": 123}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(docket=123, page=2, limit=10)

        expected_params = {
            "docket": 123,
            "page": 2,
            "limit": 10
        }
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_get_document(self):
        """Test get method for specific RECAP document."""
        mock_response = {"id": 1, "docket": 123, "docket_entry": 456, "filepath_local": "/path/to/doc.pdf"}
        self.mock_client.get.return_value = mock_response

        result = self.api.get(1)

        self.mock_client.get.assert_called_once_with("recap-documents/1/")
        assert result == mock_response

    def test_get_document_with_different_id(self):
        """Test get method with different document ID."""
        mock_response = {"id": 2, "docket": 789, "docket_entry": 101, "filepath_local": "/path/to/doc2.pdf"}
        self.mock_client.get.return_value = mock_response

        result = self.api.get(2)

        self.mock_client.get.assert_called_once_with("recap-documents/2/")
        assert result == mock_response

    def test_paginate_no_filters(self):
        """Test paginate method with no filters."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate()

        expected_params = {}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_docket_filter(self):
        """Test paginate method with docket filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(docket=123)

        expected_params = {"docket": 123}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_docket_entry_filter(self):
        """Test paginate method with docket_entry filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(docket_entry=456)

        expected_params = {"docket_entry": 456}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_court_filter(self):
        """Test paginate method with court filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(court="scotus")

        expected_params = {"court": "scotus"}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_multiple_filters(self):
        """Test paginate method with multiple filters."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(docket=123, docket_entry=456, court="scotus")

        expected_params = {
            "docket": 123,
            "docket_entry": 456,
            "court": "scotus"
        }
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_additional_kwargs(self):
        """Test paginate method with additional kwargs."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(docket=123, page=2, limit=10)

        expected_params = {
            "docket": 123,
            "page": 2,
            "limit": 10
        }
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_list_with_none_values(self):
        """Test list method with None values (should be filtered out)."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(
            docket=None,
            docket_entry=None,
            court=None
        )

        expected_params = {}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_paginate_with_none_values(self):
        """Test paginate method with None values (should be filtered out)."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(
            docket=None,
            docket_entry=None,
            court=None
        )

        expected_params = {}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator

    def test_list_with_zero_values(self):
        """Test list method with zero values (should be included)."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(docket=0, docket_entry=0)

        expected_params = {"docket": 0, "docket_entry": 0}
        self.mock_client.get.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_response

    def test_paginate_with_zero_values(self):
        """Test paginate method with zero values (should be included)."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(docket=0, docket_entry=0)

        expected_params = {"docket": 0, "docket_entry": 0}
        self.mock_client.paginate.assert_called_once_with("recap-documents/", params=expected_params)
        assert result == mock_paginator
