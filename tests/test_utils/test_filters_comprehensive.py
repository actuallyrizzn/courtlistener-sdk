"""
Comprehensive tests for filter utilities.
"""

import pytest
from datetime import date, datetime
from courtlistener.utils.filters import (
    build_filters, build_date_range_filter, build_contains_filter,
    build_in_filter, build_exact_filter, build_ordering, _format_date,
    combine_filters
)


class TestBuildFiltersComprehensive:
    """Test cases for build_filters function."""

    def test_build_filters_basic(self):
        """Test basic filter building."""
        filters = build_filters(court='scotus', date_filed__gte='2020-01-01')
        
        assert filters == {'court': 'scotus', 'date_filed__gte': '2020-01-01'}

    def test_build_filters_with_none_values(self):
        """Test that None values are filtered out."""
        filters = build_filters(
            court='scotus',
            date_filed__gte='2020-01-01',
            judge=None,
            status=None
        )
        
        assert filters == {'court': 'scotus', 'date_filed__gte': '2020-01-01'}
        assert 'judge' not in filters
        assert 'status' not in filters

    def test_build_filters_empty(self):
        """Test building filters with no arguments."""
        filters = build_filters()
        
        assert filters == {}

    def test_build_filters_with_various_types(self):
        """Test building filters with various data types."""
        filters = build_filters(
            court='scotus',
            count=5,
            active=True,
            rate=0.5,
            items=['a', 'b', 'c']
        )
        
        assert filters == {
            'court': 'scotus',
            'count': 5,
            'active': True,
            'rate': 0.5,
            'items': ['a', 'b', 'c']
        }

    def test_build_filters_with_zero_values(self):
        """Test that zero values are included."""
        filters = build_filters(count=0, rate=0.0, active=False)
        
        assert filters == {'count': 0, 'rate': 0.0, 'active': False}

    def test_build_filters_with_empty_string(self):
        """Test that empty strings are included."""
        filters = build_filters(court='', description='')
        
        assert filters == {'court': '', 'description': ''}


class TestBuildDateRangeFilterComprehensive:
    """Test cases for build_date_range_filter function."""

    def test_build_date_range_filter_both_dates(self):
        """Test with both start and end dates."""
        filters = build_date_range_filter('date_filed', '2020-01-01', '2020-12-31')
        
        assert filters == {'date_filed__range': '2020-01-01/2020-12-31'}

    def test_build_date_range_filter_start_only(self):
        """Test with start date only."""
        filters = build_date_range_filter('date_filed', '2020-01-01', None)
        
        assert filters == {'date_filed__gte': '2020-01-01'}

    def test_build_date_range_filter_end_only(self):
        """Test with end date only."""
        filters = build_date_range_filter('date_filed', None, '2020-12-31')
        
        assert filters == {'date_filed__lte': '2020-12-31'}

    def test_build_date_range_filter_no_dates(self):
        """Test with no dates."""
        filters = build_date_range_filter('date_filed', None, None)
        
        assert filters == {}

    def test_build_date_range_filter_with_date_objects(self):
        """Test with date objects."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        filters = build_date_range_filter('date_filed', start_date, end_date)
        
        assert filters == {'date_filed__range': '2020-01-01/2020-12-31'}

    def test_build_date_range_filter_with_datetime_objects(self):
        """Test with datetime objects."""
        start_datetime = datetime(2020, 1, 1, 12, 0, 0)
        end_datetime = datetime(2020, 12, 31, 23, 59, 59)
        filters = build_date_range_filter('date_filed', start_datetime, end_datetime)
        
        assert filters == {'date_filed__range': '2020-01-01T12:00:00/2020-12-31T23:59:59'}

    def test_build_date_range_filter_mixed_types(self):
        """Test with mixed date types."""
        start_date = date(2020, 1, 1)
        end_date_str = '2020-12-31'
        filters = build_date_range_filter('date_filed', start_date, end_date_str)
        
        assert filters == {'date_filed__range': '2020-01-01/2020-12-31'}

    def test_build_date_range_filter_empty_strings(self):
        """Test with empty string dates."""
        filters = build_date_range_filter('date_filed', '', '')
        
        assert filters == {}

    def test_build_date_range_filter_with_whitespace(self):
        """Test with whitespace-only dates."""
        filters = build_date_range_filter('date_filed', '   ', '   ')
        
        # The current implementation treats whitespace as valid dates
        assert filters == {'date_filed__range': '   /   '}


class TestBuildContainsFilterComprehensive:
    """Test cases for build_contains_filter function."""

    def test_build_contains_filter_case_insensitive(self):
        """Test case-insensitive contains filter."""
        filters = build_contains_filter('case_name', 'Smith', case_sensitive=False)
        
        assert filters == {'case_name__icontains': 'Smith'}

    def test_build_contains_filter_case_sensitive(self):
        """Test case-sensitive contains filter."""
        filters = build_contains_filter('case_name', 'Smith', case_sensitive=True)
        
        assert filters == {'case_name__contains': 'Smith'}

    def test_build_contains_filter_default_case_insensitive(self):
        """Test default case-insensitive behavior."""
        filters = build_contains_filter('case_name', 'Smith')
        
        assert filters == {'case_name__icontains': 'Smith'}

    def test_build_contains_filter_with_special_characters(self):
        """Test with special characters in search term."""
        filters = build_contains_filter('description', 'Smith v. Jones & Co.', case_sensitive=False)
        
        assert filters == {'description__icontains': 'Smith v. Jones & Co.'}

    def test_build_contains_filter_with_empty_string(self):
        """Test with empty search string."""
        filters = build_contains_filter('case_name', '', case_sensitive=False)
        
        assert filters == {'case_name__icontains': ''}


class TestBuildInFilterComprehensive:
    """Test cases for build_in_filter function."""

    def test_build_in_filter_basic(self):
        """Test basic in filter."""
        filters = build_in_filter('court', ['scotus', 'ca1', 'ca2'])
        
        assert filters == {'court__in': 'scotus,ca1,ca2'}

    def test_build_in_filter_single_value(self):
        """Test with single value."""
        filters = build_in_filter('court', ['scotus'])
        
        assert filters == {'court__in': 'scotus'}

    def test_build_in_filter_empty_list(self):
        """Test with empty list."""
        filters = build_in_filter('court', [])
        
        assert filters == {}

    def test_build_in_filter_with_mixed_types(self):
        """Test with mixed data types."""
        filters = build_in_filter('status', [1, 'active', True, 0.5])
        
        assert filters == {'status__in': '1,active,True,0.5'}

    def test_build_in_filter_with_none_values(self):
        """Test with None values in list."""
        filters = build_in_filter('court', ['scotus', None, 'ca1'])
        
        assert filters == {'court__in': 'scotus,None,ca1'}

    def test_build_in_filter_with_duplicates(self):
        """Test with duplicate values."""
        filters = build_in_filter('court', ['scotus', 'ca1', 'scotus'])
        
        assert filters == {'court__in': 'scotus,ca1,scotus'}


class TestBuildExactFilterComprehensive:
    """Test cases for build_exact_filter function."""

    def test_build_exact_filter_string(self):
        """Test with string value."""
        filters = build_exact_filter('docket_number', '21-123')
        
        assert filters == {'docket_number': '21-123'}

    def test_build_exact_filter_integer(self):
        """Test with integer value."""
        filters = build_exact_filter('id', 123)
        
        assert filters == {'id': 123}

    def test_build_exact_filter_boolean(self):
        """Test with boolean value."""
        filters = build_exact_filter('active', True)
        
        assert filters == {'active': True}

    def test_build_exact_filter_float(self):
        """Test with float value."""
        filters = build_exact_filter('rate', 0.5)
        
        assert filters == {'rate': 0.5}

    def test_build_exact_filter_none(self):
        """Test with None value."""
        filters = build_exact_filter('judge', None)
        
        assert filters == {'judge': None}

    def test_build_exact_filter_list(self):
        """Test with list value."""
        filters = build_exact_filter('tags', ['criminal', 'federal'])
        
        assert filters == {'tags': ['criminal', 'federal']}


class TestBuildOrderingComprehensive:
    """Test cases for build_ordering function."""

    def test_build_ordering_single_field_ascending(self):
        """Test single field ascending order."""
        ordering = build_ordering('date_filed', reverse=False)
        
        assert ordering == {'order_by': 'date_filed'}

    def test_build_ordering_single_field_descending(self):
        """Test single field descending order."""
        ordering = build_ordering('date_filed', reverse=True)
        
        assert ordering == {'order_by': '-date_filed'}

    def test_build_ordering_single_field_already_descending(self):
        """Test single field already with minus prefix."""
        ordering = build_ordering('-date_filed', reverse=True)
        
        assert ordering == {'order_by': '-date_filed'}

    def test_build_ordering_multiple_fields_ascending(self):
        """Test multiple fields ascending order."""
        ordering = build_ordering(['date_filed', 'case_name'], reverse=False)
        
        assert ordering == {'order_by': 'date_filed,case_name'}

    def test_build_ordering_multiple_fields_descending(self):
        """Test multiple fields descending order."""
        ordering = build_ordering(['date_filed', 'case_name'], reverse=True)
        
        assert ordering == {'order_by': '-date_filed,case_name'}

    def test_build_ordering_multiple_fields_mixed_prefixes(self):
        """Test multiple fields with mixed prefixes."""
        ordering = build_ordering(['-date_filed', 'case_name'], reverse=True)
        
        assert ordering == {'order_by': '-date_filed,case_name'}

    def test_build_ordering_single_field_string_list(self):
        """Test single field as string list."""
        ordering = build_ordering('date_filed', reverse=False)
        
        assert ordering == {'order_by': 'date_filed'}

    def test_build_ordering_empty_list(self):
        """Test with empty list."""
        ordering = build_ordering([], reverse=False)
        
        assert ordering == {'order_by': ''}

    def test_build_ordering_single_item_list(self):
        """Test with single item list."""
        ordering = build_ordering(['date_filed'], reverse=True)
        
        assert ordering == {'order_by': '-date_filed'}


class TestFormatDateComprehensive:
    """Test cases for _format_date function."""

    def test_format_date_string(self):
        """Test with string input."""
        result = _format_date('2020-01-01')
        
        assert result == '2020-01-01'

    def test_format_date_date_object(self):
        """Test with date object."""
        date_obj = date(2020, 1, 1)
        result = _format_date(date_obj)
        
        assert result == '2020-01-01'

    def test_format_date_datetime_object(self):
        """Test with datetime object."""
        datetime_obj = datetime(2020, 1, 1, 12, 30, 45)
        result = _format_date(datetime_obj)
        
        assert result == '2020-01-01T12:30:45'

    def test_format_date_invalid_type(self):
        """Test with invalid type."""
        with pytest.raises(ValueError, match="Invalid date type: <class 'int'>"):
            _format_date(123)

    def test_format_date_none(self):
        """Test with None input."""
        with pytest.raises(ValueError, match="Invalid date type: <class 'NoneType'>"):
            _format_date(None)

    def test_format_date_list(self):
        """Test with list input."""
        with pytest.raises(ValueError, match="Invalid date type: <class 'list'>"):
            _format_date(['2020-01-01'])


class TestCombineFiltersComprehensive:
    """Test cases for combine_filters function."""

    def test_combine_filters_basic(self):
        """Test basic filter combination."""
        filters1 = {'court': 'scotus'}
        filters2 = {'date_filed__gte': '2020-01-01'}
        filters3 = {'status': 'active'}
        
        result = combine_filters(filters1, filters2, filters3)
        
        assert result == {
            'court': 'scotus',
            'date_filed__gte': '2020-01-01',
            'status': 'active'
        }

    def test_combine_filters_single_dict(self):
        """Test with single filter dictionary."""
        filters = {'court': 'scotus', 'status': 'active'}
        
        result = combine_filters(filters)
        
        assert result == {'court': 'scotus', 'status': 'active'}

    def test_combine_filters_no_args(self):
        """Test with no arguments."""
        result = combine_filters()
        
        assert result == {}

    def test_combine_filters_empty_dicts(self):
        """Test with empty dictionaries."""
        result = combine_filters({}, {}, {})
        
        assert result == {}

    def test_combine_filters_mixed_empty(self):
        """Test with mixed empty and non-empty dictionaries."""
        filters1 = {'court': 'scotus'}
        filters2 = {}
        filters3 = {'status': 'active'}
        
        result = combine_filters(filters1, filters2, filters3)
        
        assert result == {'court': 'scotus', 'status': 'active'}

    def test_combine_filters_override_values(self):
        """Test that later dictionaries override earlier ones."""
        filters1 = {'court': 'scotus', 'status': 'inactive'}
        filters2 = {'status': 'active', 'date_filed__gte': '2020-01-01'}
        
        result = combine_filters(filters1, filters2)
        
        assert result == {
            'court': 'scotus',
            'status': 'active',  # Overridden by filters2
            'date_filed__gte': '2020-01-01'
        }

    def test_combine_filters_none_values(self):
        """Test with None values in dictionaries."""
        filters1 = {'court': 'scotus', 'judge': None}
        filters2 = {'status': 'active'}
        
        result = combine_filters(filters1, filters2)
        
        assert result == {
            'court': 'scotus',
            'judge': None,
            'status': 'active'
        }

    def test_combine_filters_complex_nested(self):
        """Test with complex nested values."""
        filters1 = {'court': 'scotus', 'tags': ['criminal', 'federal']}
        filters2 = {'date_range': {'start': '2020-01-01', 'end': '2020-12-31'}}
        
        result = combine_filters(filters1, filters2)
        
        assert result == {
            'court': 'scotus',
            'tags': ['criminal', 'federal'],
            'date_range': {'start': '2020-01-01', 'end': '2020-12-31'}
        }


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_build_filters_with_unicode(self):
        """Test with unicode characters."""
        filters = build_filters(case_name='Smith v. Jones & Co.', judge='José García')
        
        assert filters == {
            'case_name': 'Smith v. Jones & Co.',
            'judge': 'José García'
        }

    def test_build_in_filter_with_unicode(self):
        """Test in filter with unicode characters."""
        filters = build_in_filter('judge', ['José García', 'María López'])
        
        assert filters == {'judge__in': 'José García,María López'}

    def test_build_contains_filter_with_unicode(self):
        """Test contains filter with unicode characters."""
        filters = build_contains_filter('case_name', 'José García', case_sensitive=False)
        
        assert filters == {'case_name__icontains': 'José García'}

    def test_build_date_range_filter_with_unicode_field(self):
        """Test date range filter with unicode field name."""
        filters = build_date_range_filter('fecha_archivo', '2020-01-01', '2020-12-31')
        
        assert filters == {'fecha_archivo__range': '2020-01-01/2020-12-31'}

    def test_build_ordering_with_unicode_field(self):
        """Test ordering with unicode field name."""
        ordering = build_ordering('fecha_archivo', reverse=True)
        
        assert ordering == {'order_by': '-fecha_archivo'}

    def test_combine_filters_with_unicode(self):
        """Test combining filters with unicode."""
        filters1 = {'juez': 'José García'}
        filters2 = {'caso': 'Smith v. Jones'}
        
        result = combine_filters(filters1, filters2)
        
        assert result == {'juez': 'José García', 'caso': 'Smith v. Jones'}

    def test_build_filters_with_very_long_strings(self):
        """Test with very long string values."""
        long_string = 'x' * 1000
        filters = build_filters(description=long_string)
        
        assert filters == {'description': long_string}
        assert len(filters['description']) == 1000

    def test_build_in_filter_with_very_long_list(self):
        """Test in filter with very long list."""
        long_list = [f'item_{i}' for i in range(1000)]
        filters = build_in_filter('tags', long_list)
        
        assert filters == {'tags__in': ','.join(long_list)}
        assert len(filters['tags__in'].split(',')) == 1000

    def test_build_ordering_with_very_long_field_list(self):
        """Test ordering with very long field list."""
        long_fields = [f'field_{i}' for i in range(100)]
        ordering = build_ordering(long_fields, reverse=True)
        
        expected = '-' + ','.join(long_fields)
        assert ordering == {'order_by': expected}
