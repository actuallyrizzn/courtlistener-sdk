"""
CourtListener SDK (Unofficial)

An unofficial, comprehensive Python SDK for the CourtListener REST API (v4.1).
Provides easy access to legal data including case law, dockets, judges, opinions,
financial disclosures, and citation networks.

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

__version__ = "0.1.0"
__author__ = "CourtListener SDK Community"
__email__ = "actuallyrizzn@gmail.com"

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