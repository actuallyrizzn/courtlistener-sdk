"""Docket model for CourtListener SDK."""

from typing import Optional, List
from datetime import datetime, date
from .base import BaseModel


class Docket(BaseModel):
    """Model for docket data."""
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    @property
    def id(self) -> int:
        """Docket ID."""
        return getattr(self, 'id', None)
    
    @property
    def case_name(self) -> str:
        """Case name."""
        return getattr(self, 'case_name', None)
    
    @property
    def case_name_full(self) -> str:
        """Full case name."""
        return getattr(self, 'case_name_full', None)
    
    @property
    def case_name_short(self) -> str:
        """Short case name."""
        return getattr(self, 'case_name_short', None)
    
    @property
    def docket_number(self) -> str:
        """Docket number."""
        return getattr(self, 'docket_number', None)
    
    @property
    def court_id(self) -> str:
        """Court ID."""
        return getattr(self, 'court_id', None)
    
    @property
    def court(self) -> str:
        """Court URL."""
        return getattr(self, 'court', None)
    
    @property
    def court_name(self) -> str:
        """Court name."""
        return getattr(self, 'court_name', None)
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when docket was created."""
        date_str = getattr(self, 'date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when docket was last modified."""
        date_str = getattr(self, 'date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_filed(self) -> Optional[date]:
        """Date when case was filed."""
        date_str = getattr(self, 'date_filed', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_terminated(self) -> Optional[date]:
        """Date when case was terminated."""
        date_str = getattr(self, 'date_terminated', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_last_filing(self) -> Optional[date]:
        """Date of last filing."""
        date_str = getattr(self, 'date_last_filing', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def absolute_url(self) -> str:
        """Absolute URL for the docket."""
        return getattr(self, 'absolute_url', None)
    
    @property
    def pacer_case_id(self) -> Optional[str]:
        """PACER case ID."""
        return getattr(self, 'pacer_case_id', None)
    
    @property
    def pacer_case_number(self) -> str:
        """PACER case number."""
        return getattr(self, 'pacer_case_number', None)
    
    @property
    def pacer_sequence_number(self) -> Optional[int]:
        """PACER sequence number."""
        return getattr(self, 'pacer_sequence_number', None)
    
    @property
    def pacer_doc_id(self) -> Optional[str]:
        """PACER document ID."""
        return getattr(self, 'pacer_doc_id', None)
    
    @property
    def nature_of_suit(self) -> str:
        """Nature of suit."""
        return getattr(self, 'nature_of_suit', None)
    
    @property
    def cause(self) -> str:
        """Cause of action."""
        return getattr(self, 'cause', None)
    
    @property
    def jury_demand(self) -> str:
        """Jury demand."""
        return getattr(self, 'jury_demand', None)
    
    @property
    def jurisdiction_type(self) -> str:
        """Jurisdiction type."""
        return getattr(self, 'jurisdiction_type', None)
    
    @property
    def appellate_fee_status(self) -> str:
        """Appellate fee status."""
        return getattr(self, 'appellate_fee_status', None)
    
    @property
    def appellate_case_type_information(self) -> str:
        """Appellate case type information."""
        return getattr(self, 'appellate_case_type_information', None)
    
    @property
    def mdl_status(self) -> str:
        """MDL status."""
        return getattr(self, 'mdl_status', None)
    
    @property
    def filepath_local(self) -> str:
        """Local file path."""
        return getattr(self, 'filepath_local', None)
    
    @property
    def filepath_ia(self) -> str:
        """Internet Archive file path."""
        return getattr(self, 'filepath_ia', None)
    
    @property
    def filepath_ia_json(self) -> str:
        """Internet Archive JSON file path."""
        return getattr(self, 'filepath_ia_json', None)
    
    @property
    def ia_upload_failure_count(self) -> int:
        """Number of IA upload failures."""
        return getattr(self, 'ia_upload_failure_count', 0)
    
    @property
    def ia_needs_upload(self) -> bool:
        """Whether IA upload is needed."""
        return getattr(self, 'ia_needs_upload', False)
    
    @property
    def ia_date_first_good_file(self) -> Optional[date]:
        """Date of first good IA file."""
        date_str = getattr(self, 'ia_date_first_good_file', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def ia_date_last_good_file(self) -> Optional[date]:
        """Date of last good IA file."""
        date_str = getattr(self, 'ia_date_last_good_file', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def blocked(self) -> bool:
        """Whether the docket is blocked."""
        return getattr(self, 'blocked', False)
    
    @property
    def blocked_reason(self) -> str:
        """Reason for blocking."""
        return getattr(self, 'blocked_reason', None)
    
    @property
    def date_blocked(self) -> Optional[date]:
        """Date when docket was blocked."""
        date_str = getattr(self, 'date_blocked', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def appeal_from_str(self) -> str:
        """Appeal from string."""
        return getattr(self, 'appeal_from_str', None)
    
    @property
    def assigned_to_str(self) -> str:
        """Assigned to string."""
        return getattr(self, 'assigned_to_str', None)
    
    @property
    def referred_to_str(self) -> str:
        """Referred to string."""
        return getattr(self, 'referred_to_str', None)
    
    @property
    def panel_str(self) -> str:
        """Panel string."""
        return getattr(self, 'panel_str', None)
    
    @property
    def date_cert_granted(self) -> Optional[date]:
        """Date when cert was granted."""
        date_str = getattr(self, 'date_cert_granted', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_cert_denied(self) -> Optional[date]:
        """Date when cert was denied."""
        date_str = getattr(self, 'date_cert_denied', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_argued(self) -> Optional[date]:
        """Date when case was argued."""
        date_str = getattr(self, 'date_argued', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_reargued(self) -> Optional[date]:
        """Date when case was reargued."""
        date_str = getattr(self, 'date_reargued', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_reargument_denied(self) -> Optional[date]:
        """Date when reargument was denied."""
        date_str = getattr(self, 'date_reargument_denied', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the docket."""
        return getattr(self, 'resource_uri', None)
    
    def __repr__(self) -> str:
        """String representation of the docket."""
        return f"Docket(id={self.id}, case_name='{self.case_name}')"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket_number = getattr(self, 'docket_number', 'None')
            case_name = getattr(self, 'case_name', 'None')
            return f"Docket(id={self.id}, docket_number='{docket_number}', case_name='{case_name}')"
        return f"{class_name}()" 