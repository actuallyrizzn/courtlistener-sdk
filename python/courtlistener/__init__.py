"""
CourtListener SDK (Unofficial)

An unofficial, comprehensive Python SDK for the CourtListener REST API (v4.1).
Provides easy access to legal data including case law, dockets, judges, opinions,
financial disclosures, and citation networks.

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.

Copyright (C) 2024 CourtListener SDK Community

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
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