"""
Comprehensive tests for validation utilities.
"""

import pytest
from courtlistener.utils.validators import (
    validate_date, validate_citation, validate_docket_number,
    validate_court_id, validate_api_token, validate_id,
    validate_url, validate_required_field
)
from courtlistener.exceptions import ValidationError


class TestValidateDateComprehensive:
    """Test cases for validate_date function."""

    def test_validate_date_valid_formats(self):
        """Test valid date formats."""
        valid_dates = [
            '2020-01-01',
            '2023-12-31',
            '2000-02-29',  # Leap year
            '2021-06-15'
        ]
        
        for date_str in valid_dates:
            assert validate_date(date_str) is True

    def test_validate_date_invalid_formats(self):
        """Test invalid date formats."""
        invalid_dates = [
            '2020/01/01',  # Wrong separator
            '01-01-2020',  # Wrong order
            '2020-1-1',    # Missing leading zeros
            '2020-13-01',  # Invalid month
            '2020-01-32',  # Invalid day
            '2021-02-29',  # Not a leap year
            '20-01-01',    # Wrong year format
            '2020-01',     # Missing day
            '2020',        # Missing month and day
        ]
        
        for date_str in invalid_dates:
            with pytest.raises(ValidationError):
                validate_date(date_str)

    def test_validate_date_empty_string(self):
        """Test empty date string."""
        with pytest.raises(ValidationError, match="Date string cannot be empty"):
            validate_date("")

    def test_validate_date_none(self):
        """Test None date."""
        with pytest.raises(ValidationError, match="Date string cannot be empty"):
            validate_date(None)

    def test_validate_date_whitespace(self):
        """Test whitespace-only date."""
        with pytest.raises(ValidationError, match="Invalid date format"):
            validate_date("   ")


class TestValidateCitationComprehensive:
    """Test cases for validate_citation function."""

    def test_validate_citation_valid_formats(self):
        """Test valid citation formats."""
        valid_citations = [
            '576 U.S. 644',
            '576 U.S 644',
            '123 F.3d 456',
            '123 F3d 456',
            '123 F.Supp. 456',
            '123 F Supp 456',
            '123 Cal. 3d 456',
            '123 Cal 3d 456',
            'Custom Citation Format',  # Should still pass
        ]
        
        for citation in valid_citations:
            assert validate_citation(citation) is True

    def test_validate_citation_empty_string(self):
        """Test empty citation."""
        with pytest.raises(ValidationError, match="Citation cannot be empty"):
            validate_citation("")

    def test_validate_citation_none(self):
        """Test None citation."""
        with pytest.raises(ValidationError, match="Citation cannot be empty"):
            validate_citation(None)

    def test_validate_citation_whitespace_handling(self):
        """Test citation with extra whitespace."""
        citation = "  576  U.S.  644  "
        assert validate_citation(citation) is True


class TestValidateDocketNumberComprehensive:
    """Test cases for validate_docket_number function."""

    def test_validate_docket_number_valid_formats(self):
        """Test valid docket number formats."""
        valid_dockets = [
            '21-123',           # SCOTUS
            '1:21-cv-12345',    # Federal
            'CR-21-12345',      # State
            '123',              # Simple number
            'Custom-Docket-123', # Custom format
        ]
        
        for docket in valid_dockets:
            assert validate_docket_number(docket) is True

    def test_validate_docket_number_empty_string(self):
        """Test empty docket number."""
        with pytest.raises(ValidationError, match="Docket number cannot be empty"):
            validate_docket_number("")

    def test_validate_docket_number_none(self):
        """Test None docket number."""
        with pytest.raises(ValidationError, match="Docket number cannot be empty"):
            validate_docket_number(None)


class TestValidateCourtIdComprehensive:
    """Test cases for validate_court_id function."""

    def test_validate_court_id_valid_formats(self):
        """Test valid court ID formats."""
        valid_court_ids = [
            'scotus',
            'ca1',
            'ca2',
            'ca-dc',
            'ca-1',
            '123',
            'court-123',
        ]
        
        for court_id in valid_court_ids:
            assert validate_court_id(court_id) is True

    def test_validate_court_id_invalid_formats(self):
        """Test invalid court ID formats."""
        invalid_court_ids = [
            'SCOTUS',  # Uppercase
            'CA 1',    # Space
            'ca@1',    # Special character
            'ca.1',    # Period
        ]
        
        for court_id in invalid_court_ids:
            with pytest.raises(ValidationError, match="Invalid court ID format"):
                validate_court_id(court_id)

    def test_validate_court_id_empty_string(self):
        """Test empty court ID."""
        with pytest.raises(ValidationError, match="Court ID cannot be empty"):
            validate_court_id("")

    def test_validate_court_id_none(self):
        """Test None court ID."""
        with pytest.raises(ValidationError, match="Court ID cannot be empty"):
            validate_court_id(None)


class TestValidateApiTokenComprehensive:
    """Test cases for validate_api_token function."""

    def test_validate_api_token_valid(self):
        """Test valid API token."""
        valid_tokens = [
            '1234567890',
            'abcdefghijklmnop',
            'token123456789',
        ]
        
        for token in valid_tokens:
            assert validate_api_token(token) is True

    def test_validate_api_token_too_short(self):
        """Test API token that's too short."""
        with pytest.raises(ValidationError, match="API token appears too short"):
            validate_api_token("123456789")

    def test_validate_api_token_empty_string(self):
        """Test empty API token."""
        with pytest.raises(ValidationError, match="API token cannot be empty"):
            validate_api_token("")

    def test_validate_api_token_none(self):
        """Test None API token."""
        with pytest.raises(ValidationError, match="API token cannot be empty"):
            validate_api_token(None)


class TestValidateIdComprehensive:
    """Test cases for validate_id function."""

    def test_validate_id_valid_integer(self):
        """Test valid integer ID."""
        valid_ids = [1, 123, 999999]
        
        for id_val in valid_ids:
            assert validate_id(id_val) is True

    def test_validate_id_valid_string(self):
        """Test valid string ID."""
        valid_ids = ['1', '123', '999999']
        
        for id_val in valid_ids:
            assert validate_id(id_val) is True

    def test_validate_id_invalid_integer(self):
        """Test invalid integer ID."""
        invalid_ids = [0, -1, -123]
        
        for id_val in invalid_ids:
            with pytest.raises(ValidationError, match="ID must be a positive integer"):
                validate_id(id_val)

    def test_validate_id_invalid_string(self):
        """Test invalid string ID."""
        invalid_ids = ['0', '-1', '-123', 'abc', '12.5']
        
        for id_val in invalid_ids:
            with pytest.raises(ValidationError):
                validate_id(id_val)

    def test_validate_id_none(self):
        """Test None ID."""
        with pytest.raises(ValidationError, match="ID cannot be None"):
            validate_id(None)

    def test_validate_id_empty_string(self):
        """Test empty string ID."""
        with pytest.raises(ValidationError, match="ID string cannot be empty"):
            validate_id("")

    def test_validate_id_whitespace_string(self):
        """Test whitespace-only string ID."""
        with pytest.raises(ValidationError, match="ID string cannot be empty"):
            validate_id("   ")

    def test_validate_id_invalid_type(self):
        """Test invalid type for ID."""
        with pytest.raises(ValidationError, match="ID must be int or str"):
            validate_id(1.5)

    def test_validate_id_list_type(self):
        """Test list type for ID."""
        with pytest.raises(ValidationError, match="ID must be int or str"):
            validate_id([1, 2, 3])


class TestValidateUrlComprehensive:
    """Test cases for validate_url function."""

    def test_validate_url_valid_formats(self):
        """Test valid URL formats."""
        valid_urls = [
            'https://example.com',
            'http://example.com',
            'https://api.courtlistener.com/api/rest/v4/',
            'https://example.com/path?query=value',
            'https://example.com/path#fragment',
        ]
        
        for url in valid_urls:
            assert validate_url(url) is True

    def test_validate_url_invalid_formats(self):
        """Test invalid URL formats."""
        invalid_urls = [
            'example.com',      # Missing protocol
            'ftp://example.com', # Wrong protocol
            'https://',         # Missing domain
            'https://example.com ', # Trailing space
        ]
        
        for url in invalid_urls:
            with pytest.raises(ValidationError, match="Invalid URL format"):
                validate_url(url)

    def test_validate_url_empty_string(self):
        """Test empty URL."""
        with pytest.raises(ValidationError, match="URL cannot be empty"):
            validate_url("")

    def test_validate_url_none(self):
        """Test None URL."""
        with pytest.raises(ValidationError, match="URL cannot be empty"):
            validate_url(None)


class TestValidateRequiredFieldComprehensive:
    """Test cases for validate_required_field function."""

    def test_validate_required_field_valid_values(self):
        """Test valid required field values."""
        valid_values = [
            'string',
            '123',
            '0',
            [],
            {},
            True,
            False,
            0,
            123,
        ]
        
        for value in valid_values:
            assert validate_required_field(value, 'test_field') is True

    def test_validate_required_field_none(self):
        """Test None value."""
        with pytest.raises(ValidationError, match="test_field is required"):
            validate_required_field(None, 'test_field')

    def test_validate_required_field_empty_string(self):
        """Test empty string value."""
        with pytest.raises(ValidationError, match="test_field cannot be empty"):
            validate_required_field("", 'test_field')

    def test_validate_required_field_whitespace_string(self):
        """Test whitespace-only string value."""
        with pytest.raises(ValidationError, match="test_field cannot be empty"):
            validate_required_field("   ", 'test_field')

    def test_validate_required_field_custom_field_name(self):
        """Test with custom field name."""
        with pytest.raises(ValidationError, match="custom_field is required"):
            validate_required_field(None, 'custom_field')

    def test_validate_required_field_empty_string_custom_name(self):
        """Test empty string with custom field name."""
        with pytest.raises(ValidationError, match="custom_field cannot be empty"):
            validate_required_field("", 'custom_field')


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_validate_date_edge_cases(self):
        """Test date validation edge cases."""
        # Test February 29 in leap year
        assert validate_date('2020-02-29') is True
        
        # Test February 29 in non-leap year
        with pytest.raises(ValidationError):
            validate_date('2021-02-29')

    def test_validate_citation_edge_cases(self):
        """Test citation validation edge cases."""
        # Test citation with special characters
        assert validate_citation('Smith v. Jones & Co., 123 F.3d 456') is True
        
        # Test very long citation
        long_citation = 'A' * 1000
        assert validate_citation(long_citation) is True

    def test_validate_docket_number_edge_cases(self):
        """Test docket number validation edge cases."""
        # Test very long docket number
        long_docket = 'A' * 1000
        assert validate_docket_number(long_docket) is True

    def test_validate_court_id_edge_cases(self):
        """Test court ID validation edge cases."""
        # Test very long court ID
        long_court_id = 'a' * 1000
        assert validate_court_id(long_court_id) is True

    def test_validate_api_token_edge_cases(self):
        """Test API token validation edge cases."""
        # Test exactly 10 characters (should pass - >= 10 is valid)
        assert validate_api_token('1234567890') is True
        
        # Test 11 characters (should pass)
        assert validate_api_token('12345678901') is True

    def test_validate_id_edge_cases(self):
        """Test ID validation edge cases."""
        # Test very large integer
        assert validate_id(999999999999) is True
        
        # Test very large string integer
        assert validate_id('999999999999') is True

    def test_validate_url_edge_cases(self):
        """Test URL validation edge cases."""
        # Test URL with very long path
        long_url = 'https://example.com/' + 'a' * 1000
        assert validate_url(long_url) is True

    def test_validate_required_field_edge_cases(self):
        """Test required field validation edge cases."""
        # Test with very long string
        long_string = 'a' * 1000
        assert validate_required_field(long_string, 'test_field') is True
        
        # Test with complex object
        complex_obj = {'key': 'value', 'nested': [1, 2, 3]}
        assert validate_required_field(complex_obj, 'test_field') is True
