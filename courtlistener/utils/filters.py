"""
Filter utilities for building Django-style query parameters.
"""

from typing import Dict, Any, Optional, Union, List
from datetime import date, datetime


def build_filters(**kwargs) -> Dict[str, Any]:
    """
    Build Django-style filters for API queries.
    
    Args:
        **kwargs: Filter parameters (e.g., court='scotus', date_filed__gte='2020-01-01')
    
    Returns:
        Dictionary of filter parameters
    
    Examples:
        >>> build_filters(court='scotus', date_filed__gte='2020-01-01')
        {'court': 'scotus', 'date_filed__gte': '2020-01-01'}
    """
    filters = {}
    
    for key, value in kwargs.items():
        if value is not None:
            filters[key] = value
    
    return filters


def build_date_range_filter(
    field: str,
    start_date: Optional[Union[str, date, datetime]] = None,
    end_date: Optional[Union[str, date, datetime]] = None
) -> Dict[str, str]:
    """
    Build a date range filter for a field.
    
    Args:
        field: Field name to filter on
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
    
    Returns:
        Dictionary with date range filter
    
    Examples:
        >>> build_date_range_filter('date_filed', '2020-01-01', '2020-12-31')
        {'date_filed__range': '2020-01-01/2020-12-31'}
    """
    if start_date is None and end_date is None:
        return {}
    
    # Convert dates to ISO format strings
    start_str = _format_date(start_date) if start_date else ''
    end_str = _format_date(end_date) if end_date else ''
    
    if start_str and end_str:
        return {f"{field}__range": f"{start_str}/{end_str}"}
    elif start_str:
        return {f"{field}__gte": start_str}
    elif end_str:
        return {f"{field}__lte": end_str}
    
    return {}


def build_contains_filter(field: str, value: str, case_sensitive: bool = False) -> Dict[str, str]:
    """
    Build a contains filter for text fields.
    
    Args:
        field: Field name to filter on
        value: Value to search for
        case_sensitive: Whether the search should be case sensitive
    
    Returns:
        Dictionary with contains filter
    
    Examples:
        >>> build_contains_filter('case_name', 'Smith', case_sensitive=False)
        {'case_name__icontains': 'Smith'}
    """
    suffix = 'contains' if case_sensitive else 'icontains'
    return {f"{field}__{suffix}": value}


def build_in_filter(field: str, values: List[Any]) -> Dict[str, str]:
    """
    Build an 'in' filter for matching multiple values.
    
    Args:
        field: Field name to filter on
        values: List of values to match
    
    Returns:
        Dictionary with 'in' filter
    
    Examples:
        >>> build_in_filter('court', ['scotus', 'ca1'])
        {'court__in': 'scotus,ca1'}
    """
    if not values:
        return {}
    
    # Convert values to comma-separated string
    value_str = ','.join(str(v) for v in values)
    return {f"{field}__in": value_str}


def build_exact_filter(field: str, value: Any) -> Dict[str, Any]:
    """
    Build an exact match filter.
    
    Args:
        field: Field name to filter on
        value: Exact value to match
    
    Returns:
        Dictionary with exact filter
    
    Examples:
        >>> build_exact_filter('docket_number', '21-123')
        {'docket_number': '21-123'}
    """
    return {field: value}


def build_ordering(ordering: Union[str, List[str]], reverse: bool = False) -> Dict[str, str]:
    """
    Build ordering parameters.
    
    Args:
        ordering: Field(s) to order by
        reverse: Whether to reverse the order (descending)
    
    Returns:
        Dictionary with ordering parameter
    
    Examples:
        >>> build_ordering('date_filed', reverse=True)
        {'order_by': '-date_filed'}
    """
    if isinstance(ordering, list):
        ordering_str = ','.join(ordering)
    else:
        ordering_str = ordering
    
    if reverse:
        # Add minus prefix for descending order
        if ordering_str.startswith('-'):
            # Already descending
            pass
        else:
            ordering_str = f"-{ordering_str}"
    
    return {'order_by': ordering_str}


def _format_date(date_obj: Union[str, date, datetime]) -> str:
    """Convert date object to ISO format string."""
    if isinstance(date_obj, str):
        return date_obj
    elif isinstance(date_obj, (date, datetime)):
        return date_obj.isoformat()
    else:
        raise ValueError(f"Invalid date type: {type(date_obj)}")


def combine_filters(*filter_dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combine multiple filter dictionaries.
    
    Args:
        *filter_dicts: Filter dictionaries to combine
    
    Returns:
        Combined filter dictionary
    
    Examples:
        >>> filters1 = {'court': 'scotus'}
        >>> filters2 = {'date_filed__gte': '2020-01-01'}
        >>> combine_filters(filters1, filters2)
        {'court': 'scotus', 'date_filed__gte': '2020-01-01'}
    """
    combined = {}
    for filter_dict in filter_dicts:
        if filter_dict:
            combined.update(filter_dict)
    return combined 