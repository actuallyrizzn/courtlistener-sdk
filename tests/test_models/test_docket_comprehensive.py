"""Comprehensive tests for Docket model."""

import pytest
from courtlistener.models.docket import Docket


class TestDocketComprehensive:
    """Comprehensive tests for Docket model."""

    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "case_name": "Test Case"}
        docket = Docket(data)
        assert docket._data == data

    def test_docket_id_property(self):
        """Test docket_id property."""
        data = {"id": 123}
        docket = Docket(data)
        assert docket.docket_id == 123

    def test_docket_id_property_none(self):
        """Test docket_id property when not set."""
        data = {}
        docket = Docket(data)
        assert docket.docket_id is None

    def test_id_property(self):
        """Test id property (alias for docket_id)."""
        data = {"id": 456}
        docket = Docket(data)
        assert docket.id == 456

    def test_case_name_property(self):
        """Test case_name property."""
        data = {"case_name": "Smith v. Jones"}
        docket = Docket(data)
        assert docket.case_name == "Smith v. Jones"

    def test_case_name_property_default(self):
        """Test case_name property with default."""
        data = {}
        docket = Docket(data)
        assert docket.case_name == "Unknown Case"

    def test_case_name_full_property(self):
        """Test case_name_full property."""
        data = {"case_name_full": "John Smith v. Mary Jones"}
        docket = Docket(data)
        assert docket.case_name_full == "John Smith v. Mary Jones"

    def test_case_name_short_property(self):
        """Test case_name_short property."""
        data = {"case_name_short": "Smith v. Jones"}
        docket = Docket(data)
        assert docket.case_name_short == "Smith v. Jones"

    def test_docket_number_property(self):
        """Test docket_number property."""
        data = {"docket_number": "1:23-cv-456"}
        docket = Docket(data)
        assert docket.docket_number == "1:23-cv-456"

    def test_court_id_property(self):
        """Test court_id property."""
        data = {"court_id": "scotus"}
        docket = Docket(data)
        assert docket.court_id == "scotus"

    def test_court_property(self):
        """Test court property."""
        data = {"court": "Supreme Court"}
        docket = Docket(data)
        assert docket.court == "Supreme Court"

    def test_date_filed_property(self):
        """Test date_filed property."""
        data = {"date_filed": "2023-01-15"}
        docket = Docket(data)
        assert docket.date_filed == "2023-01-15"

    def test_date_terminated_property(self):
        """Test date_terminated property."""
        data = {"date_terminated": "2023-12-31"}
        docket = Docket(data)
        assert docket.date_terminated == "2023-12-31"

    def test_date_created_property(self):
        """Test date_created property."""
        data = {"date_created": "2023-01-01T12:00:00Z"}
        docket = Docket(data)
        assert docket.date_created == "2023-01-01T12:00:00Z"

    def test_date_modified_property(self):
        """Test date_modified property."""
        data = {"date_modified": "2023-01-15T10:30:00Z"}
        docket = Docket(data)
        assert docket.date_modified == "2023-01-15T10:30:00Z"

    def test_absolute_url_property(self):
        """Test absolute_url property."""
        data = {"absolute_url": "http://example.com/docket/1"}
        docket = Docket(data)
        assert docket.absolute_url == "http://example.com/docket/1"

    def test_resource_uri_property(self):
        """Test resource_uri property."""
        data = {"resource_uri": "http://api.example.com/docket/1/"}
        docket = Docket(data)
        assert docket.resource_uri == "http://api.example.com/docket/1/"

    def test_is_terminated_property_true(self):
        """Test is_terminated property when terminated."""
        data = {"date_terminated": "2023-12-31"}
        docket = Docket(data)
        assert docket.is_terminated is True

    def test_is_terminated_property_false(self):
        """Test is_terminated property when not terminated."""
        data = {}
        docket = Docket(data)
        assert docket.is_terminated is False

    def test_has_audio_property_true(self):
        """Test has_audio property when audio exists."""
        data = {"audio_count": 5}
        docket = Docket(data)
        assert docket.has_audio is True

    def test_has_audio_property_false(self):
        """Test has_audio property when no audio."""
        data = {}
        docket = Docket(data)
        assert docket.has_audio is False

    def test_has_audio_property_zero(self):
        """Test has_audio property when audio_count is 0."""
        data = {"audio_count": 0}
        docket = Docket(data)
        assert docket.has_audio is False

    def test_has_opinions_property_true(self):
        """Test has_opinions property when opinions exist."""
        data = {"opinion_count": 3}
        docket = Docket(data)
        assert docket.has_opinions is True

    def test_has_opinions_property_false(self):
        """Test has_opinions property when no opinions."""
        data = {}
        docket = Docket(data)
        assert docket.has_opinions is False

    def test_has_opinions_property_zero(self):
        """Test has_opinions property when opinion_count is 0."""
        data = {"opinion_count": 0}
        docket = Docket(data)
        assert docket.has_opinions is False

    def test_has_recap_property_true(self):
        """Test has_recap property when recap exists."""
        data = {"recap_count": 10}
        docket = Docket(data)
        assert docket.has_recap is True

    def test_has_recap_property_false(self):
        """Test has_recap property when no recap."""
        data = {}
        docket = Docket(data)
        assert docket.has_recap is False

    def test_has_recap_property_zero(self):
        """Test has_recap property when recap_count is 0."""
        data = {"recap_count": 0}
        docket = Docket(data)
        assert docket.has_recap is False

    def test_comprehensive_data(self):
        """Test with comprehensive data."""
        data = {
            "id": 1,
            "case_name": "Smith v. Jones",
            "case_name_full": "John Smith v. Mary Jones",
            "case_name_short": "Smith v. Jones",
            "docket_number": "1:23-cv-456",
            "court_id": "scotus",
            "court": "Supreme Court",
            "date_filed": "2023-01-15",
            "date_terminated": "2023-12-31",
            "date_created": "2023-01-01T12:00:00Z",
            "date_modified": "2023-01-15T10:30:00Z",
            "absolute_url": "http://example.com/docket/1",
            "resource_uri": "http://api.example.com/docket/1/",
            "audio_count": 5,
            "opinion_count": 3,
            "recap_count": 10
        }
        docket = Docket(data)
        
        # Test all properties
        assert docket.docket_id == 1
        assert docket.id == 1
        assert docket.case_name == "Smith v. Jones"
        assert docket.case_name_full == "John Smith v. Mary Jones"
        assert docket.case_name_short == "Smith v. Jones"
        assert docket.docket_number == "1:23-cv-456"
        assert docket.court_id == "scotus"
        assert docket.court == "Supreme Court"
        assert docket.date_filed == "2023-01-15"
        assert docket.date_terminated == "2023-12-31"
        assert docket.date_created == "2023-01-01T12:00:00Z"
        assert docket.date_modified == "2023-01-15T10:30:00Z"
        assert docket.absolute_url == "http://example.com/docket/1"
        assert docket.resource_uri == "http://api.example.com/docket/1/"
        assert docket.is_terminated is True
        assert docket.has_audio is True
        assert docket.has_opinions is True
        assert docket.has_recap is True

    def test_edge_case_empty_data(self):
        """Test with completely empty data."""
        data = {}
        docket = Docket(data)
        
        # All properties should have defaults or be None
        assert docket.docket_id is None
        assert docket.id is None
        assert docket.case_name == "Unknown Case"
        assert docket.case_name_full == ""
        assert docket.case_name_short == ""
        assert docket.docket_number is None
        assert docket.court_id is None
        assert docket.court is None
        assert docket.date_filed is None
        assert docket.date_terminated is None
        assert docket.date_created is None
        assert docket.date_modified is None
        assert docket.absolute_url is None
        assert docket.resource_uri is None
        assert docket.is_terminated is False
        assert docket.has_audio is False
        assert docket.has_opinions is False
        assert docket.has_recap is False

    def test_edge_case_partial_data(self):
        """Test with partial data."""
        data = {"id": 1, "case_name": "Test Case"}
        docket = Docket(data)
        
        # Set properties should have values
        assert docket.docket_id == 1
        assert docket.id == 1
        assert docket.case_name == "Test Case"
        
        # Unset properties should have defaults
        assert docket.case_name_full == ""
        assert docket.case_name_short == ""
        assert docket.docket_number is None
        assert docket.court_id is None
        assert docket.court is None
        assert docket.is_terminated is False
        assert docket.has_audio is False
        assert docket.has_opinions is False
        assert docket.has_recap is False
