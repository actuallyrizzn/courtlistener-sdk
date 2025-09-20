"""
Comprehensive tests for the validators utility module.
"""

import pytest
from courtlistener.utils.validators import (
    validate_date,
    validate_citation,
    validate_docket_number,
    validate_court_id,
    validate_api_token,
    validate_id,
    validate_url,
    validate_required_field
)
from courtlistener.exceptions import ValidationError


class TestValidateDate:
    """Test cases for validate_date function."""

    def test_validate_date_valid_format(self):
        """Test valid date format."""
        result = validate_date('2023-01-01')
        assert result is True

    def test_validate_date_invalid_format(self):
        """Test invalid date format."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            validate_date('01/01/2023')

    def test_validate_date_invalid_date(self):
        """Test invalid date (leap year)."""
        with pytest.raises(ValidationError, match="Invalid date"):
            validate_date('2023-02-29')

    def test_validate_date_empty_string(self):
        """Test empty date string."""
        with pytest.raises(ValidationError, match="Date string cannot be empty"):
            validate_date('')

    def test_validate_date_none(self):
        """Test None date."""
        with pytest.raises(ValidationError, match="Date string cannot be empty"):
            validate_date(None)

    def test_validate_date_wrong_length(self):
        """Test date with wrong length."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            validate_date('2023-1-1')

    def test_validate_date_non_numeric(self):
        """Test date with non-numeric characters."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            validate_date('2023-01-xx')


class TestValidateCitation:
    """Test cases for validate_citation function."""

    def test_validate_citation_scotus(self):
        """Test SCOTUS citation format."""
        result = validate_citation('576 U.S. 644')
        assert result is True

    def test_validate_citation_scotus_no_periods(self):
        """Test SCOTUS citation without periods."""
        result = validate_citation('576 US 644')
        assert result is True

    def test_validate_citation_federal_reporter(self):
        """Test Federal Reporter citation format."""
        result = validate_citation('123 F.3d 456')
        assert result is True

    def test_validate_citation_federal_supplement(self):
        """Test Federal Supplement citation format."""
        result = validate_citation('123 F.Supp. 456')
        assert result is True

    def test_validate_citation_state(self):
        """Test state citation format."""
        result = validate_citation('123 Cal. 3d 456')
        assert result is True

    def test_validate_citation_empty(self):
        """Test empty citation."""
        with pytest.raises(ValidationError, match="Citation cannot be empty"):
            validate_citation('')

    def test_validate_citation_none(self):
        """Test None citation."""
        with pytest.raises(ValidationError, match="Citation cannot be empty"):
            validate_citation(None)

    def test_validate_citation_extra_spaces(self):
        """Test citation with extra spaces."""
        result = validate_citation('  576  U.S.  644  ')
        assert result is True

    def test_validate_citation_non_standard(self):
        """Test non-standard citation (should still pass)."""
        result = validate_citation('Some random citation format')
        assert result is True


class TestValidateDocketNumber:
    """Test cases for validate_docket_number function."""

    def test_validate_docket_number_scotus(self):
        """Test SCOTUS docket number format."""
        result = validate_docket_number('21-123')
        assert result is True

    def test_validate_docket_number_federal(self):
        """Test federal docket number format."""
        result = validate_docket_number('1:21-cv-12345')
        assert result is True

    def test_validate_docket_number_state(self):
        """Test state docket number format."""
        result = validate_docket_number('CR-21-12345')
        assert result is True

    def test_validate_docket_number_simple(self):
        """Test simple numeric docket number."""
        result = validate_docket_number('12345')
        assert result is True

    def test_validate_docket_number_empty(self):
        """Test empty docket number."""
        with pytest.raises(ValidationError, match="Docket number cannot be empty"):
            validate_docket_number('')

    def test_validate_docket_number_none(self):
        """Test None docket number."""
        with pytest.raises(ValidationError, match="Docket number cannot be empty"):
            validate_docket_number(None)

    def test_validate_docket_number_non_standard(self):
        """Test non-standard docket number (should still pass)."""
        result = validate_docket_number('ABC-123-XYZ')
        assert result is True


class TestValidateCourtId:
    """Test cases for validate_court_id function."""

    def test_validate_court_id_valid(self):
        """Test valid court ID."""
        result = validate_court_id('scotus')
        assert result is True

    def test_validate_court_id_with_hyphens(self):
        """Test court ID with hyphens."""
        result = validate_court_id('ca-1')
        assert result is True

    def test_validate_court_id_with_numbers(self):
        """Test court ID with numbers."""
        result = validate_court_id('ca1')
        assert result is True

    def test_validate_court_id_mixed(self):
        """Test court ID with mixed characters."""
        result = validate_court_id('ca-1-2')
        assert result is True

    def test_validate_court_id_empty(self):
        """Test empty court ID."""
        with pytest.raises(ValidationError, match="Court ID cannot be empty"):
            validate_court_id('')

    def test_validate_court_id_none(self):
        """Test None court ID."""
        with pytest.raises(ValidationError, match="Court ID cannot be empty"):
            validate_court_id(None)

    def test_validate_court_id_uppercase(self):
        """Test court ID with uppercase letters."""
        with pytest.raises(ValidationError, match="Invalid court ID format"):
            validate_court_id('SCOTUS')

    def test_validate_court_id_special_chars(self):
        """Test court ID with special characters."""
        with pytest.raises(ValidationError, match="Invalid court ID format"):
            validate_court_id('ca.1')


class TestValidateApiToken:
    """Test cases for validate_api_token function."""

    def test_validate_api_token_valid(self):
        """Test valid API token."""
        result = validate_api_token('abcdefghijklmnopqrstuvwxyz1234567890')
        assert result is True

    def test_validate_api_token_minimum_length(self):
        """Test API token with minimum length."""
        result = validate_api_token('1234567890')
        assert result is True

    def test_validate_api_token_too_short(self):
        """Test API token that's too short."""
        with pytest.raises(ValidationError, match="API token appears too short"):
            validate_api_token('123456789')

    def test_validate_api_token_empty(self):
        """Test empty API token."""
        with pytest.raises(ValidationError, match="API token cannot be empty"):
            validate_api_token('')

    def test_validate_api_token_none(self):
        """Test None API token."""
        with pytest.raises(ValidationError, match="API token cannot be empty"):
            validate_api_token(None)


class TestValidateId:
    """Test cases for validate_id function."""

    def test_validate_id_positive_integer(self):
        """Test positive integer ID."""
        result = validate_id(123)
        assert result is True

    def test_validate_id_positive_string_integer(self):
        """Test positive string integer ID."""
        result = validate_id('123')
        assert result is True

    def test_validate_id_zero(self):
        """Test zero ID (should fail)."""
        with pytest.raises(ValidationError, match="ID must be a positive integer"):
            validate_id(0)

    def test_validate_id_negative_integer(self):
        """Test negative integer ID."""
        with pytest.raises(ValidationError, match="ID must be a positive integer"):
            validate_id(-1)

    def test_validate_id_negative_string(self):
        """Test negative string ID."""
        with pytest.raises(ValidationError, match="ID must be a positive integer"):
            validate_id('-1')

    def test_validate_id_none(self):
        """Test None ID."""
        with pytest.raises(ValidationError, match="ID cannot be None"):
            validate_id(None)

    def test_validate_id_empty_string(self):
        """Test empty string ID."""
        with pytest.raises(ValidationError, match="ID string cannot be empty"):
            validate_id('')

    def test_validate_id_non_numeric_string(self):
        """Test non-numeric string ID."""
        with pytest.raises(ValidationError, match="Invalid ID format"):
            validate_id('abc')

    def test_validate_id_invalid_type(self):
        """Test invalid type ID."""
        with pytest.raises(ValidationError, match="ID must be int or str"):
            validate_id(1.5)


class TestValidateUrl:
    """Test cases for validate_url function."""

    def test_validate_url_http(self):
        """Test valid HTTP URL."""
        result = validate_url('http://example.com')
        assert result is True

    def test_validate_url_https(self):
        """Test valid HTTPS URL."""
        result = validate_url('https://example.com')
        assert result is True

    def test_validate_url_with_path(self):
        """Test URL with path."""
        result = validate_url('https://example.com/path/to/resource')
        assert result is True

    def test_validate_url_with_query(self):
        """Test URL with query parameters."""
        result = validate_url('https://example.com?param=value&other=123')
        assert result is True

    def test_validate_url_with_fragment(self):
        """Test URL with fragment."""
        result = validate_url('https://example.com#section')
        assert result is True

    def test_validate_url_empty(self):
        """Test empty URL."""
        with pytest.raises(ValidationError, match="URL cannot be empty"):
            validate_url('')

    def test_validate_url_none(self):
        """Test None URL."""
        with pytest.raises(ValidationError, match="URL cannot be empty"):
            validate_url(None)

    def test_validate_url_invalid_protocol(self):
        """Test URL with invalid protocol."""
        with pytest.raises(ValidationError, match="Invalid URL format"):
            validate_url('ftp://example.com')

    def test_validate_url_no_protocol(self):
        """Test URL without protocol."""
        with pytest.raises(ValidationError, match="Invalid URL format"):
            validate_url('example.com')

    def test_validate_url_invalid_format(self):
        """Test URL with invalid format."""
        with pytest.raises(ValidationError, match="Invalid URL format"):
            validate_url('not-a-url')


class TestValidateRequiredField:
    """Test cases for validate_required_field function."""

    def test_validate_required_field_valid_string(self):
        """Test valid string field."""
        result = validate_required_field('valid string', 'field_name')
        assert result is True

    def test_validate_required_field_valid_integer(self):
        """Test valid integer field."""
        result = validate_required_field(123, 'field_name')
        assert result is True

    def test_validate_required_field_valid_boolean(self):
        """Test valid boolean field."""
        result = validate_required_field(True, 'field_name')
        assert result is True

    def test_validate_required_field_none(self):
        """Test None field."""
        with pytest.raises(ValidationError, match="field_name is required"):
            validate_required_field(None, 'field_name')

    def test_validate_required_field_empty_string(self):
        """Test empty string field."""
        with pytest.raises(ValidationError, match="field_name cannot be empty"):
            validate_required_field('', 'field_name')

    def test_validate_required_field_whitespace_string(self):
        """Test whitespace-only string field."""
        with pytest.raises(ValidationError, match="field_name cannot be empty"):
            validate_required_field('   ', 'field_name')

    def test_validate_required_field_zero(self):
        """Test zero value (should be valid)."""
        result = validate_required_field(0, 'field_name')
        assert result is True

    def test_validate_required_field_false(self):
        """Test False value (should be valid)."""
        result = validate_required_field(False, 'field_name')
        assert result is True