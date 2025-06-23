"""
API endpoint modules for the CourtListener SDK.
"""

from .search import SearchAPI
from .dockets import DocketsAPI
from .opinions import OpinionsAPI
from .judges import JudgesAPI
from .courts import CourtsAPI
from .parties import PartiesAPI
from .attorneys import AttorneysAPI
from .documents import DocumentsAPI
from .audio import AudioAPI
from .financial import FinancialAPI
from .citations import CitationsAPI

__all__ = [
    "SearchAPI",
    "DocketsAPI",
    "OpinionsAPI",
    "JudgesAPI",
    "CourtsAPI",
    "PartiesAPI",
    "AttorneysAPI",
    "DocumentsAPI",
    "AudioAPI",
    "FinancialAPI",
    "CitationsAPI",
] 