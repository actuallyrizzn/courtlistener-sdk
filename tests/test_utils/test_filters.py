import pytest
from datetime import date, datetime
from courtlistener.utils.filters import (
    build_filters, build_date_range_filter, build_contains_filter,
    build_in_filter, build_exact_filter, build_ordering, combine_filters,
    _format_date
)


class TestBuildFilters:
    def test_build_filters_basic(self):
        """Test basic filter building."""
        filters = build_filters(court='scotus', date_filed__gte='2020-01-01')
        assert filters == {'court': 'scotus', 'date_filed__gte': '2020-01-01'}
    
    def test_build_filters_with_none_values(self):
        """Test that None values are filtered out."""
        filters = build_filters(court='scotus', date_filed=None, judge='smith')
        assert filters == {'court': 'scotus', 'judge': 'smith'}
    
    def test_build_filters_empty(self):
        """Test building filters with no arguments."""
        filters = build_filters()
        assert filters == {}


class TestBuildDateRangeFilter:
    def test_build_date_range_filter_both_dates(self):
        """Test date range filter with both start and end dates."""
        filters = build_date_range_filter('date_filed', '2020-01-01', '2020-12-31')
        assert filters == {'date_filed__range': '2020-01-01/2020-12-31'}
    
    def test_build_date_range_filter_start_only(self):
        """Test date range filter with only start date."""
        filters = build_date_range_filter('date_filed', '2020-01-01')
        assert filters == {'date_filed__gte': '2020-01-01'}
    
    def test_build_date_range_filter_end_only(self):
        """Test date range filter with only end date."""
        filters = build_date_range_filter('date_filed', end_date='2020-12-31')
        assert filters == {'date_filed__lte': '2020-12-31'}
    
    def test_build_date_range_filter_no_dates(self):
        """Test date range filter with no dates."""
        filters = build_date_range_filter('date_filed')
        assert filters == {}
    
    def test_build_date_range_filter_with_date_objects(self):
        """Test date range filter with date objects."""
        start_date = date(2020, 1, 1)
        end_date = date(2020, 12, 31)
        filters = build_date_range_filter('date_filed', start_date, end_date)
        assert filters == {'date_filed__range': '2020-01-01/2020-12-31'}
    
    def test_build_date_range_filter_with_datetime_objects(self):
        """Test date range filter with datetime objects."""
        start_date = datetime(2020, 1, 1, 12, 0, 0)
        end_date = datetime(2020, 12, 31, 23, 59, 59)
        filters = build_date_range_filter('date_filed', start_date, end_date)
        assert filters == {'date_filed__range': '2020-01-01T12:00:00/2020-12-31T23:59:59'}


class TestBuildContainsFilter:
    def test_build_contains_filter_case_sensitive(self):
        """Test case-sensitive contains filter."""
        filters = build_contains_filter('case_name', 'Smith', case_sensitive=True)
        assert filters == {'case_name__contains': 'Smith'}
    
    def test_build_contains_filter_case_insensitive(self):
        """Test case-insensitive contains filter."""
        filters = build_contains_filter('case_name', 'Smith', case_sensitive=False)
        assert filters == {'case_name__icontains': 'Smith'}
    
    def test_build_contains_filter_default_case_insensitive(self):
        """Test default case-insensitive behavior."""
        filters = build_contains_filter('case_name', 'Smith')
        assert filters == {'case_name__icontains': 'Smith'}


class TestBuildInFilter:
    def test_build_in_filter_with_values(self):
        """Test 'in' filter with multiple values."""
        filters = build_in_filter('court', ['scotus', 'ca1', 'ca2'])
        assert filters == {'court__in': 'scotus,ca1,ca2'}
    
    def test_build_in_filter_empty_list(self):
        """Test 'in' filter with empty list."""
        filters = build_in_filter('court', [])
        assert filters == {}
    
    def test_build_in_filter_mixed_types(self):
        """Test 'in' filter with mixed data types."""
        filters = build_in_filter('id', [1, '2', 3])
        assert filters == {'id__in': '1,2,3'}


class TestBuildExactFilter:
    def test_build_exact_filter_string(self):
        """Test exact filter with string value."""
        filters = build_exact_filter('docket_number', '21-123')
        assert filters == {'docket_number': '21-123'}
    
    def test_build_exact_filter_integer(self):
        """Test exact filter with integer value."""
        filters = build_exact_filter('court_id', 1)
        assert filters == {'court_id': 1}
    
    def test_build_exact_filter_boolean(self):
        """Test exact filter with boolean value."""
        filters = build_exact_filter('active', True)
        assert filters == {'active': True}


class TestBuildOrdering:
    def test_build_ordering_single_field(self):
        """Test ordering with single field."""
        filters = build_ordering('date_filed')
        assert filters == {'order_by': 'date_filed'}
    
    def test_build_ordering_single_field_reverse(self):
        """Test ordering with single field in reverse."""
        filters = build_ordering('date_filed', reverse=True)
        assert filters == {'order_by': '-date_filed'}
    
    def test_build_ordering_multiple_fields(self):
        """Test ordering with multiple fields."""
        filters = build_ordering(['date_filed', 'case_name'])
        assert filters == {'order_by': 'date_filed,case_name'}
    
    def test_build_ordering_multiple_fields_reverse(self):
        """Test ordering with multiple fields in reverse."""
        filters = build_ordering(['date_filed', 'case_name'], reverse=True)
        assert filters == {'order_by': '-date_filed,case_name'}
    
    def test_build_ordering_already_reversed(self):
        """Test ordering with field already marked as reverse."""
        filters = build_ordering('-date_filed', reverse=True)
        assert filters == {'order_by': '-date_filed'}


class TestCombineFilters:
    def test_combine_filters_multiple_dicts(self):
        """Test combining multiple filter dictionaries."""
        filters1 = {'court': 'scotus'}
        filters2 = {'date_filed__gte': '2020-01-01'}
        filters3 = {'judge': 'smith'}
        
        combined = combine_filters(filters1, filters2, filters3)
        expected = {
            'court': 'scotus',
            'date_filed__gte': '2020-01-01',
            'judge': 'smith'
        }
        assert combined == expected
    
    def test_combine_filters_with_empty_dicts(self):
        """Test combining filters with empty dictionaries."""
        filters1 = {'court': 'scotus'}
        filters2 = {}
        filters3 = {'judge': 'smith'}
        
        combined = combine_filters(filters1, filters2, filters3)
        expected = {'court': 'scotus', 'judge': 'smith'}
        assert combined == expected
    
    def test_combine_filters_overlapping_keys(self):
        """Test combining filters with overlapping keys (later wins)."""
        filters1 = {'court': 'scotus', 'judge': 'smith'}
        filters2 = {'court': 'ca1', 'date_filed': '2020-01-01'}
        
        combined = combine_filters(filters1, filters2)
        expected = {'court': 'ca1', 'judge': 'smith', 'date_filed': '2020-01-01'}
        assert combined == expected
    
    def test_combine_filters_no_dicts(self):
        """Test combining no filter dictionaries."""
        combined = combine_filters()
        assert combined == {}


class TestFormatDate:
    def test_format_date_string(self):
        """Test formatting date string."""
        result = _format_date('2020-01-01')
        assert result == '2020-01-01'
    
    def test_format_date_date_object(self):
        """Test formatting date object."""
        date_obj = date(2020, 1, 1)
        result = _format_date(date_obj)
        assert result == '2020-01-01'
    
    def test_format_date_datetime_object(self):
        """Test formatting datetime object."""
        datetime_obj = datetime(2020, 1, 1, 12, 30, 45)
        result = _format_date(datetime_obj)
        assert result == '2020-01-01T12:30:45'
    
    def test_format_date_invalid_type(self):
        """Test formatting invalid date type."""
        with pytest.raises(ValueError, match="Invalid date type"):
            _format_date(123) 