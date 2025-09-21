"""
Comprehensive tests for the People API module.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.people import PeopleAPI


class TestPeopleAPI:
    """Test cases for PeopleAPI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = PeopleAPI(self.mock_client)

    def test_init(self):
        """Test PeopleAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.endpoint == "people/"

    def test_list_no_filters(self):
        """Test list method with no filters."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list()

        expected_params = {}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_name_filter(self):
        """Test list method with name filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(name="John Doe")

        expected_params = {"name": "John Doe"}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_name_icontains_filter(self):
        """Test list method with name__icontains filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(name__icontains="John")

        expected_params = {"name__icontains": "John"}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_court_filter(self):
        """Test list method with court filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(court="scotus")

        expected_params = {"court": "scotus"}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_position_type_filter(self):
        """Test list method with position_type filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(position_type="Judge")

        expected_params = {"position_type": "Judge"}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_active_filter(self):
        """Test list method with active filter."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(active=True)

        expected_params = {"active": True}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_multiple_filters(self):
        """Test list method with multiple filters."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(
            name="John Doe",
            court="scotus",
            position_type="Judge",
            active=True
        )

        expected_params = {
            "name": "John Doe",
            "court": "scotus",
            "position_type": "Judge",
            "active": True
        }
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_list_with_additional_kwargs(self):
        """Test list method with additional kwargs."""
        mock_response = {"count": 1, "results": [{"id": 1, "name": "John Doe"}]}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(name="John Doe", page=2, limit=10)

        expected_params = {
            "name": "John Doe",
            "page": 2,
            "limit": 10
        }
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_get_person(self):
        """Test get method for specific person."""
        mock_response = {"id": 1, "name": "John Doe", "position_type": "Judge"}
        self.mock_client.get.return_value = mock_response

        result = self.api.get(1)

        self.mock_client.get.assert_called_once_with("people/1/")
        assert result == mock_response

    def test_get_person_with_different_id(self):
        """Test get method with different person ID."""
        mock_response = {"id": 2, "name": "Jane Smith", "position_type": "Justice"}
        self.mock_client.get.return_value = mock_response

        result = self.api.get(2)

        self.mock_client.get.assert_called_once_with("people/2/")
        assert result == mock_response

    def test_paginate_no_filters(self):
        """Test paginate method with no filters."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate()

        expected_params = {}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_name_filter(self):
        """Test paginate method with name filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(name="John Doe")

        expected_params = {"name": "John Doe"}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_name_icontains_filter(self):
        """Test paginate method with name__icontains filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(name__icontains="John")

        expected_params = {"name__icontains": "John"}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_court_filter(self):
        """Test paginate method with court filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(court="scotus")

        expected_params = {"court": "scotus"}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_position_type_filter(self):
        """Test paginate method with position_type filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(position_type="Judge")

        expected_params = {"position_type": "Judge"}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_active_filter(self):
        """Test paginate method with active filter."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(active=True)

        expected_params = {"active": True}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_multiple_filters(self):
        """Test paginate method with multiple filters."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(
            name="John Doe",
            court="scotus",
            position_type="Judge",
            active=True
        )

        expected_params = {
            "name": "John Doe",
            "court": "scotus",
            "position_type": "Judge",
            "active": True
        }
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_paginate_with_additional_kwargs(self):
        """Test paginate method with additional kwargs."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(name="John Doe", page=2, limit=10)

        expected_params = {
            "name": "John Doe",
            "page": 2,
            "limit": 10
        }
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator

    def test_list_with_none_values(self):
        """Test list method with None values (should be filtered out)."""
        mock_response = {"count": 0, "results": []}
        self.mock_client.get.return_value = mock_response

        result = self.api.list(
            name=None,
            name__icontains=None,
            court=None,
            position_type=None,
            active=None
        )

        expected_params = {}
        self.mock_client.get.assert_called_once_with("people/", params=expected_params)
        assert result == mock_response

    def test_paginate_with_none_values(self):
        """Test paginate method with None values (should be filtered out)."""
        mock_paginator = Mock()
        self.mock_client.paginate.return_value = mock_paginator

        result = self.api.paginate(
            name=None,
            name__icontains=None,
            court=None,
            position_type=None,
            active=None
        )

        expected_params = {}
        self.mock_client.paginate.assert_called_once_with("people/", params=expected_params)
        assert result == mock_paginator
