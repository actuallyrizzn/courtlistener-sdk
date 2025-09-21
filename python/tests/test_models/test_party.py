"""
Comprehensive tests for the Party model class.
"""

import pytest
from datetime import datetime
from courtlistener.models.party import Party


class TestParty:
    """Test cases for Party class."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {
            "id": 1,
            "name": "John Doe",
            "type": "plaintiff",
            "docket": 123,
            "terminated": False
        }
        party = Party(data)
        assert party.id == 1
        assert party.name == "John Doe"
        assert party.type == "plaintiff"
        assert party.docket == 123
        assert party.terminated is False

    def test_init_with_date_terminated(self):
        """Test initialization with date_terminated."""
        data = {
            "id": 1,
            "name": "John Doe",
            "type": "defendant",
            "date_terminated": "2023-01-01T12:30:45"
        }
        party = Party(data)
        assert party.id == 1
        assert party.name == "John Doe"
        assert party.type == "defendant"
        assert isinstance(party.date_terminated, datetime)
        assert party.date_terminated.year == 2023
        assert party.date_terminated.month == 1
        assert party.date_terminated.day == 1

    def test_init_with_attorneys(self):
        """Test initialization with attorneys list."""
        data = {
            "id": 1,
            "name": "John Doe",
            "type": "plaintiff",
            "attorneys": [
                {"id": 101, "name": "Attorney 1"},
                {"id": 102, "name": "Attorney 2"}
            ]
        }
        party = Party(data)
        assert party.id == 1
        assert party.name == "John Doe"
        assert party.type == "plaintiff"
        assert len(party.attorneys) == 2
        # Note: Attorney model might not be available, so we test the structure
        assert hasattr(party, 'attorneys')

    def test_init_sets_default_fields(self):
        """Test that default fields are set to None."""
        data = {"id": 1}
        party = Party(data)
        assert party.id == 1
        assert party.name is None
        assert party.type is None
        assert party.docket is None
        assert party.date_terminated is None
        assert party.terminated is None
        assert party.absolute_url is None
        assert party.resource_uri is None
        assert party.attorney is None

    def test_is_terminated_with_date_terminated(self):
        """Test is_terminated property with date_terminated."""
        data = {
            "id": 1,
            "date_terminated": "2023-01-01T12:30:45"
        }
        party = Party(data)
        assert party.is_terminated is True

    def test_is_terminated_with_terminated_flag(self):
        """Test is_terminated property with terminated flag."""
        data = {
            "id": 1,
            "terminated": True
        }
        party = Party(data)
        assert party.is_terminated is True

    def test_is_terminated_false(self):
        """Test is_terminated property when not terminated."""
        data = {
            "id": 1,
            "terminated": False
        }
        party = Party(data)
        assert party.is_terminated is False

    def test_is_terminated_none_values(self):
        """Test is_terminated property with None values."""
        data = {"id": 1}
        party = Party(data)
        assert party.is_terminated is False

    def test_repr_with_all_fields(self):
        """Test __repr__ with all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "type": "plaintiff",
            "docket": 123
        }
        party = Party(data)
        expected = "<Party(id=1, name='John Doe', type='plaintiff', docket=123)>"
        assert repr(party) == expected

    def test_repr_with_missing_fields(self):
        """Test __repr__ with missing fields."""
        data = {"id": 1}
        party = Party(data)
        expected = "<Party(id=1, name='Unknown', type='Unknown', docket=None)>"
        assert repr(party) == expected

    def test_repr_without_id(self):
        """Test __repr__ without id."""
        data = {"name": "John Doe"}
        party = Party(data)
        expected = "<Party()>"
        assert repr(party) == expected

    def test_str_with_all_fields(self):
        """Test __str__ with all fields."""
        data = {
            "id": 1,
            "name": "John Doe",
            "type": "plaintiff"
        }
        party = Party(data)
        expected = "Party(id=1, name='John Doe', type='plaintiff')"
        assert str(party) == expected

    def test_str_with_missing_fields(self):
        """Test __str__ with missing fields."""
        data = {"id": 1}
        party = Party(data)
        expected = "Party(id=1, name='Unknown', type='Unknown')"
        assert str(party) == expected

    def test_str_without_id(self):
        """Test __str__ without id."""
        data = {"name": "John Doe"}
        party = Party(data)
        expected = "Party()"
        assert str(party) == expected

    def test_parse_data_calls_super(self):
        """Test that _parse_data calls super()._parse_data()."""
        data = {"id": 1, "name": "John Doe"}
        party = Party(data)
        # Should have the common fields from BaseModel
        assert party.id == 1
        assert party.name == "John Doe"

    def test_parse_data_with_invalid_date(self):
        """Test _parse_data with invalid date format."""
        data = {
            "id": 1,
            "date_terminated": "invalid-date"
        }
        party = Party(data)
        # Should handle invalid date gracefully
        assert party.date_terminated is None

    def test_parse_data_with_empty_date(self):
        """Test _parse_data with empty date."""
        data = {
            "id": 1,
            "date_terminated": ""
        }
        party = Party(data)
        assert party.date_terminated is None

    def test_parse_data_with_none_date(self):
        """Test _parse_data with None date."""
        data = {
            "id": 1,
            "date_terminated": None
        }
        party = Party(data)
        assert party.date_terminated is None

    def test_parse_data_with_non_list_attorneys(self):
        """Test _parse_data with non-list attorneys."""
        data = {
            "id": 1,
            "attorneys": "not-a-list"
        }
        party = Party(data)
        # Should not crash and attorneys should remain as-is
        assert party.attorneys == "not-a-list"

    def test_parse_data_with_empty_attorneys_list(self):
        """Test _parse_data with empty attorneys list."""
        data = {
            "id": 1,
            "attorneys": []
        }
        party = Party(data)
        assert party.attorneys == []

    def test_parse_data_without_attorneys(self):
        """Test _parse_data without attorneys field."""
        data = {"id": 1}
        party = Party(data)
        # Should not have attorneys attribute
        assert not hasattr(party, 'attorneys')