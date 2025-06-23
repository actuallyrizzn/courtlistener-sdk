"""
CourtListener SDK

A comprehensive Python SDK for the CourtListener REST API (v4.1).
Provides easy access to legal data including case law, dockets, judges, opinions,
financial disclosures, and citation networks.
"""

__version__ = "0.1.0"
__author__ = "CourtListener SDK Team"
__email__ = "support@courtlistener.com"

from .client import CourtListenerClient
from .exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    APIError,
)

__all__ = [
    "CourtListenerClient",
    "CourtListenerError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
    "APIError",
] 