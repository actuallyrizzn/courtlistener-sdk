"""
Custom exceptions for the CourtListener SDK.
"""

from typing import Optional


class CourtListenerError(Exception):
    """Base exception for all CourtListener SDK errors."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(CourtListenerError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", status_code: int = 401):
        super().__init__(message, status_code)


class RateLimitError(CourtListenerError):
    """Raised when rate limits are exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", status_code: int = 429, retry_after: Optional[int] = None):
        """
        Initialize RateLimitError.
        
        Args:
            message: Error message
            status_code: HTTP status code (default 429)
            retry_after: Number of seconds to wait before retrying (from Retry-After header)
        """
        super().__init__(message, status_code)
        self.retry_after = retry_after


class NotFoundError(CourtListenerError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str = "Resource not found", status_code: int = 404):
        super().__init__(message, status_code)


class ValidationError(CourtListenerError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str = "Validation failed", status_code: int = 400):
        super().__init__(message, status_code)


class APIError(CourtListenerError):
    """Raised for general API errors."""
    
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


class ConnectionError(CourtListenerError):
    """Raised when connection to the API fails."""
    
    def __init__(self, message: str = "Connection failed"):
        super().__init__(message)


class TimeoutError(CourtListenerError):
    """Raised when API requests timeout."""
    
    def __init__(self, message: str = "Request timeout"):
        super().__init__(message)


class AcceptedError(CourtListenerError):
    """Raised when HTTP 202 Accepted is returned (async processing)."""
    
    def __init__(self, message: str = "Request accepted and being processed", retry_after: Optional[int] = None):
        """
        Initialize AcceptedError.
        
        Args:
            message: Error message
            retry_after: Number of seconds to wait before retrying (from Retry-After header)
        """
        super().__init__(message)
        self.retry_after = retry_after 