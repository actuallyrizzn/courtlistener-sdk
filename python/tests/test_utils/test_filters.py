"""
Comprehensive tests for the filters utility module.
"""

import pytest
from datetime import date, datetime
from courtlistener.utils.filters import (
    build_filters,
    build_date_range_filter,
    build_contains_filter,
    build_in_filter,
    build_exact_filter,
    build_ordering,
    _format_date,
    combine_filters
)


class TestBuildFilters:
    """Test cases for build_filters function."""

    def test_build_filters_basic(self):
        """Test basic filter building."""
        result = build_filters(court='scotus', date_filed='2023-01-01')
        expected = {'court': 'scotus', 'date_filed': '2023-01-01'}
        assert result == expected

    def test_build_filters_with_none_values(self):
        """Test that None values are filtered out."""
        result = build_filters(court='scotus', date_filed=None, active=True)
        expected = {'court': 'scotus', 'active': True}
        assert result == expected

    def test_build_filters_empty(self):
        """Test building filters with no arguments."""
        result = build_filters()
        assert result == {}

    def test_build_filters_with_django_lookups(self):
        """Test building filters with Django-style lookups."""
        result = build_filters(
            court='scotus',
            date_filed__gte='2023-01-01',
            date_filed__lte='2023-12-31',
            case_name__icontains='constitutional'
        )
        expected = {
            'court': 'scotus',
            'date_filed__gte': '2023-01-01',
            'date_filed__lte': '2023-12-31',
            'case_name__icontains': 'constitutional'
        }
        assert result == expected

    def test_build_filters_all_none_values(self):
        """Test building filters with all None values."""
        result = build_filters(court=None, date_filed=None, active=None)
        assert result == {}


class TestBuildDateRangeFilter:
    """Test cases for build_date_range_filter function."""

    def test_build_date_range_filter_both_dates(self):
        """Test date range filter with both start and end dates."""
        result = build_date_range_filter('date_filed', '2023-01-01', '2023-12-31')
        expected = {'date_filed__range': '2023-01-01/2023-12-31'}
        assert result == expected

    def test_build_date_range_filter_start_only(self):
        """Test date range filter with start date only."""
        result = build_date_range_filter('date_filed', '2023-01-01', None)
        expected = {'date_filed__gte': '2023-01-01'}
        assert result == expected

    def test_build_date_range_filter_end_only(self):
        """Test date range filter with end date only."""
        result = build_date_range_filter('date_filed', None, '2023-12-31')
        expected = {'date_filed__lte': '2023-12-31'}
        assert result == expected

    def test_build_date_range_filter_no_dates(self):
        """Test date range filter with no dates."""
        result = build_date_range_filter('date_filed', None, None)
        assert result == {}

    def test_build_date_range_filter_with_date_objects(self):
        """Test date range filter with date objects."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)
        result = build_date_range_filter('date_filed', start_date, end_date)
        expected = {'date_filed__range': '2023-01-01/2023-12-31'}
        assert result == expected

    def test_build_date_range_filter_with_datetime_objects(self):
        """Test date range filter with datetime objects."""
        start_datetime = datetime(2023, 1, 1, 12, 0, 0)
        end_datetime = datetime(2023, 12, 31, 23, 59, 59)
        result = build_date_range_filter('date_filed', start_datetime, end_datetime)
        expected = {'date_filed__range': '2023-01-01T12:00:00/2023-12-31T23:59:59'}
        assert result == expected


class TestBuildContainsFilter:
    """Test cases for build_contains_filter function."""

    def test_build_contains_filter_case_insensitive(self):
        """Test contains filter with case insensitive search."""
        result = build_contains_filter('case_name', 'Smith', case_sensitive=False)
        expected = {'case_name__icontains': 'Smith'}
        assert result == expected

    def test_build_contains_filter_case_sensitive(self):
        """Test contains filter with case sensitive search."""
        result = build_contains_filter('case_name', 'Smith', case_sensitive=True)
        expected = {'case_name__contains': 'Smith'}
        assert result == expected

    def test_build_contains_filter_default_case_insensitive(self):
        """Test contains filter defaults to case insensitive."""
        result = build_contains_filter('case_name', 'Smith')
        expected = {'case_name__icontains': 'Smith'}
        assert result == expected


class TestBuildInFilter:
    """Test cases for build_in_filter function."""

    def test_build_in_filter_basic(self):
        """Test basic in filter building."""
        result = build_in_filter('court', ['scotus', 'ca1', 'ca2'])
        expected = {'court__in': 'scotus,ca1,ca2'}
        assert result == expected

    def test_build_in_filter_empty_list(self):
        """Test in filter with empty list."""
        result = build_in_filter('court', [])
        assert result == {}

    def test_build_in_filter_single_item(self):
        """Test in filter with single item."""
        result = build_in_filter('court', ['scotus'])
        expected = {'court__in': 'scotus'}
        assert result == expected

    def test_build_in_filter_mixed_types(self):
        """Test in filter with mixed types."""
        result = build_in_filter('id', [1, 2, '3', 4])
        expected = {'id__in': '1,2,3,4'}
        assert result == expected


class TestBuildExactFilter:
    """Test cases for build_exact_filter function."""

    def test_build_exact_filter_string(self):
        """Test exact filter with string value."""
        result = build_exact_filter('docket_number', '21-123')
        expected = {'docket_number': '21-123'}
        assert result == expected

    def test_build_exact_filter_integer(self):
        """Test exact filter with integer value."""
        result = build_exact_filter('id', 123)
        expected = {'id': 123}
        assert result == expected

    def test_build_exact_filter_boolean(self):
        """Test exact filter with boolean value."""
        result = build_exact_filter('active', True)
        expected = {'active': True}
        assert result == expected


class TestBuildOrdering:
    """Test cases for build_ordering function."""

    def test_build_ordering_single_field(self):
        """Test ordering with single field."""
        result = build_ordering('date_filed')
        expected = {'order_by': 'date_filed'}
        assert result == expected

    def test_build_ordering_single_field_reverse(self):
        """Test ordering with single field in reverse."""
        result = build_ordering('date_filed', reverse=True)
        expected = {'order_by': '-date_filed'}
        assert result == expected

    def test_build_ordering_multiple_fields(self):
        """Test ordering with multiple fields."""
        result = build_ordering(['date_filed', 'case_name'])
        expected = {'order_by': 'date_filed,case_name'}
        assert result == expected

    def test_build_ordering_multiple_fields_reverse(self):
        """Test ordering with multiple fields in reverse."""
        result = build_ordering(['date_filed', 'case_name'], reverse=True)
        expected = {'order_by': '-date_filed,case_name'}
        assert result == expected

    def test_build_ordering_already_descending(self):
        """Test ordering with already descending field."""
        result = build_ordering('-date_filed', reverse=True)
        expected = {'order_by': '-date_filed'}
        assert result == expected

    def test_build_ordering_mixed_descending(self):
        """Test ordering with mixed descending fields."""
        result = build_ordering(['-date_filed', 'case_name'], reverse=True)
        expected = {'order_by': '-date_filed,case_name'}
        assert result == expected


class TestFormatDate:
    """Test cases for _format_date function."""

    def test_format_date_string(self):
        """Test formatting string date."""
        result = _format_date('2023-01-01')
        assert result == '2023-01-01'

    def test_format_date_date_object(self):
        """Test formatting date object."""
        date_obj = date(2023, 1, 1)
        result = _format_date(date_obj)
        assert result == '2023-01-01'

    def test_format_date_datetime_object(self):
        """Test formatting datetime object."""
        datetime_obj = datetime(2023, 1, 1, 12, 30, 45)
        result = _format_date(datetime_obj)
        assert result == '2023-01-01T12:30:45'

    def test_format_date_invalid_type(self):
        """Test formatting invalid date type."""
        with pytest.raises(ValueError, match="Invalid date type"):
            _format_date(123)


class TestCombineFilters:
    """Test cases for combine_filters function."""

    def test_combine_filters_basic(self):
        """Test basic filter combination."""
        filters1 = {'court': 'scotus'}
        filters2 = {'date_filed__gte': '2023-01-01'}
        result = combine_filters(filters1, filters2)
        expected = {'court': 'scotus', 'date_filed__gte': '2023-01-01'}
        assert result == expected

    def test_combine_filters_multiple(self):
        """Test combining multiple filter dictionaries."""
        filters1 = {'court': 'scotus'}
        filters2 = {'date_filed__gte': '2023-01-01'}
        filters3 = {'case_name__icontains': 'constitutional'}
        result = combine_filters(filters1, filters2, filters3)
        expected = {
            'court': 'scotus',
            'date_filed__gte': '2023-01-01',
            'case_name__icontains': 'constitutional'
        }
        assert result == expected

    def test_combine_filters_empty(self):
        """Test combining empty filter dictionaries."""
        result = combine_filters({}, {}, {})
        assert result == {}

    def test_combine_filters_with_none(self):
        """Test combining filters with None values."""
        filters1 = {'court': 'scotus'}
        filters2 = None
        filters3 = {'date_filed__gte': '2023-01-01'}
        result = combine_filters(filters1, filters2, filters3)
        expected = {'court': 'scotus', 'date_filed__gte': '2023-01-01'}
        assert result == expected

    def test_combine_filters_overlapping_keys(self):
        """Test combining filters with overlapping keys (later wins)."""
        filters1 = {'court': 'scotus', 'active': True}
        filters2 = {'court': 'ca1', 'date_filed': '2023-01-01'}
        result = combine_filters(filters1, filters2)
        expected = {'court': 'ca1', 'active': True, 'date_filed': '2023-01-01'}
        assert result == expected

    def test_combine_filters_no_args(self):
        """Test combining filters with no arguments."""
        result = combine_filters()
        assert result == {}