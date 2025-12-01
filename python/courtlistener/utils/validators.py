"""
Validation utilities for the CourtListener SDK.
"""

import re
from typing import Optional, Union
from datetime import date, datetime
from ..exceptions import ValidationError


def validate_date(date_str: str) -> bool:
    """
    Validate date string format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If date format is invalid
    """
    if not date_str:
        raise ValidationError("Date string cannot be empty")
    
    # Check format YYYY-MM-DD
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        raise ValidationError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD")
    
    try:
        # Validate that it's a real date
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError as e:
        raise ValidationError(f"Invalid date: {date_str}. {str(e)}")


def validate_citation(citation: str) -> bool:
    """
    Validate legal citation format.
    
    Supports common citation formats including:
    - SCOTUS: "576 U.S. 644" or "576 US 644"
    - Federal Reporter: "123 F.3d 456" or "123 F3d 456" or "123 F. 3d 456"
    - Federal Supplement: "123 F.Supp. 456" or "123 F Supp 456"
    - Federal Appendix: "123 F.App'x 456"
    - State citations: "123 Cal. 3d 456" or "123 N.Y. 456"
    
    Args:
        citation: Citation string to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If citation format is invalid
    """
    if not citation:
        raise ValidationError("Citation cannot be empty")
    
    # Normalize whitespace
    citation_clean = re.sub(r'\s+', ' ', citation.strip())
    
    # Comprehensive citation patterns
    patterns = [
        # SCOTUS: 576 U.S. 644 or 576 US 644
        r'^\d+\s+U\.?S\.?\s+\d+$',
        # Federal Reporter: 123 F.3d 456, 123 F3d 456, 123 F. 3d 456
        r'^\d+\s+F\.?\s*\d*d\s+\d+$',
        # Federal Supplement: 123 F.Supp. 456, 123 F Supp 456, 123 F. Supp. 456
        r'^\d+\s+F\.?\s*Supp\.?\s+\d+$',
        # Federal Appendix: 123 F.App'x 456, 123 F Appx 456
        r'^\d+\s+F\.?\s*App[\'\.]?x\s+\d+$',
        # State citations with series: 123 Cal. 3d 456, 123 N.Y. 2d 456
        r'^\d+\s+[A-Za-z]+\.?\s+\d+d\s+\d+$',
        # State citations without series: 123 Cal. 456, 123 N.Y. 456
        r'^\d+\s+[A-Za-z]+\.?\s+\d+$',
    ]
    
    for pattern in patterns:
        if re.match(pattern, citation_clean):
            return True
    
    # If no pattern matches, raise validation error
    raise ValidationError(
        f"Invalid citation format: '{citation}'. "
        f"Expected formats include: '576 U.S. 644', '123 F.3d 456', '123 F.Supp. 456', "
        f"'123 Cal. 3d 456', or similar standard legal citation formats."
    )


def validate_docket_number(docket_number: str) -> bool:
    """
    Validate docket number format.
    
    Supports common docket number formats including:
    - SCOTUS: "21-123"
    - Federal District: "1:21-cv-12345" or "1-21-cv-12345"
    - Federal Circuit: "21-1234"
    - State: "CR-21-12345" or "CV-2021-12345"
    - Simple numeric: "12345"
    
    Args:
        docket_number: Docket number to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If docket number format is invalid
    """
    if not docket_number:
        raise ValidationError("Docket number cannot be empty")
    
    # Comprehensive docket number patterns
    patterns = [
        # SCOTUS: 21-123
        r'^\d+-\d+$',
        # Federal District with colon: 1:21-cv-12345, 1:21-cr-12345, 1:21-mc-12345
        r'^\d+:\d+-(cv|cr|mc|md|mi|mj|bk|ap)-\d+$',
        # Federal District with hyphen: 1-21-cv-12345, 1-21-cr-12345
        r'^\d+-\d+-(cv|cr|mc|md|mi|mj|bk|ap)-\d+$',
        # Federal Circuit: 21-1234, 21-12345
        r'^\d+-\d{4,}$',
        # State with prefix: CR-21-12345, CV-2021-12345, CA-21-12345
        r'^[A-Z]{1,4}-\d{2,4}-\d+$',
        # Simple numeric: 12345
        r'^\d+$',
    ]
    
    for pattern in patterns:
        if re.match(pattern, docket_number, re.IGNORECASE):
            return True
    
    # If no pattern matches, raise validation error
    raise ValidationError(
        f"Invalid docket number format: '{docket_number}'. "
        f"Expected formats include: '21-123' (SCOTUS), '1:21-cv-12345' (Federal), "
        f"'CR-21-12345' (State), or numeric formats."
    )


def validate_court_id(court_id: str) -> bool:
    """
    Validate court ID format.
    
    Args:
        court_id: Court ID to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If court ID format is invalid
    """
    if not court_id:
        raise ValidationError("Court ID cannot be empty")
    
    # Court IDs are typically lowercase alphanumeric with hyphens
    pattern = r'^[a-z0-9-]+$'
    if not re.match(pattern, court_id):
        raise ValidationError(f"Invalid court ID format: {court_id}")
    
    return True


def validate_api_token(token: str) -> bool:
    """
    Validate API token format.
    
    Args:
        token: API token to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If token format is invalid
    """
    if not token:
        raise ValidationError("API token cannot be empty")
    
    # API tokens are typically alphanumeric
    if len(token) < 10:
        raise ValidationError("API token appears too short")
    
    return True


def validate_id(id_value: Union[int, str]) -> bool:
    """
    Validate ID value.
    
    Args:
        id_value: ID to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If ID format is invalid
    """
    if id_value is None:
        raise ValidationError("ID cannot be None")
    
    if isinstance(id_value, int):
        if id_value <= 0:
            raise ValidationError("ID must be a positive integer")
    elif isinstance(id_value, str):
        if not id_value.strip():
            raise ValidationError("ID string cannot be empty")
        try:
            int_val = int(id_value)
            if int_val <= 0:
                raise ValidationError("ID must be a positive integer")
        except ValueError:
            raise ValidationError(f"Invalid ID format: {id_value}")
    else:
        raise ValidationError(f"ID must be int or str, got {type(id_value)}")
    
    return True


def validate_url(url: str) -> bool:
    """
    Validate URL format.
    
    Args:
        url: URL to validate
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If URL format is invalid
    """
    if not url:
        raise ValidationError("URL cannot be empty")
    
    # Basic URL pattern
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    if not re.match(pattern, url):
        raise ValidationError(f"Invalid URL format: {url}")
    
    return True


def validate_required_field(value: any, field_name: str) -> bool:
    """
    Validate that a required field is not None or empty.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
    
    Returns:
        True if valid, raises ValidationError if invalid
    
    Raises:
        ValidationError: If field is None or empty
    """
    if value is None:
        raise ValidationError(f"{field_name} is required")
    
    if isinstance(value, str) and not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")
    
    return True 