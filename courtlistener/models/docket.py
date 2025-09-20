"""Docket model for CourtListener SDK."""

from typing import Optional, List
from datetime import datetime, date
from .base import BaseModel


class Docket(BaseModel):
    """Model for docket data."""
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    @property
    def docket_id(self) -> int:
        """Docket ID."""
        return self._data.get('id', None)
    
    @property
    def id(self) -> int:
        """Docket ID (alias for docket_id)."""
        return self._data.get('id', None)
    
    @property
    def case_name(self) -> str:
        """Case name."""
        return self._data.get('case_name', 'Unknown Case')
    
    @property
    def case_name_full(self) -> str:
        """Full case name."""
        return self._data.get('case_name_full', '')
    
    @property
    def case_name_short(self) -> str:
        """Short case name."""
        return self._data.get('case_name_short', '')
    
    @property
    def docket_number(self) -> str:
        """Docket number."""
        return self._data.get('docket_number', None)
    
    @property
    def court_id(self) -> str:
        """Court ID."""
        return self._data.get('court_id', None)
    
    @property
    def court(self) -> str:
        """Court URL."""
        return self._data.get('court', None)
    
    @property
    def court_name(self) -> str:
        """Court name."""
        return self._data.get('court_name', None)
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when docket was created."""
        date_str = self._data.get('date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when docket was last modified."""
        date_str = self._data.get('date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_filed(self) -> Optional[date]:
        """Date when case was filed."""
        date_str = self._data.get('date_filed', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_terminated(self) -> Optional[date]:
        """Date when case was terminated."""
        date_str = self._data.get('date_terminated', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_last_filing(self) -> Optional[date]:
        """Date of last filing."""
        date_str = self._data.get('date_last_filing', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def absolute_url(self) -> str:
        """Absolute URL for the docket."""
        return self._data.get('absolute_url', None)
    
    @property
    def pacer_case_id(self) -> Optional[str]:
        """PACER case ID."""
        return self._data.get('pacer_case_id', None)
    
    @property
    def pacer_case_number(self) -> str:
        """PACER case number."""
        return self._data.get('pacer_case_number', None)
    
    @property
    def pacer_sequence_number(self) -> Optional[int]:
        """PACER sequence number."""
        return self._data.get('pacer_sequence_number', None)
    
    @property
    def pacer_doc_id(self) -> Optional[str]:
        """PACER document ID."""
        return self._data.get('pacer_doc_id', None)
    
    @property
    def nature_of_suit(self) -> str:
        """Nature of suit."""
        return self._data.get('nature_of_suit', None)
    
    @property
    def cause(self) -> str:
        """Cause of action."""
        return self._data.get('cause', None)
    
    @property
    def jury_demand(self) -> str:
        """Jury demand."""
        return self._data.get('jury_demand', None)
    
    @property
    def jurisdiction_type(self) -> str:
        """Jurisdiction type."""
        return self._data.get('jurisdiction_type', None)
    
    @property
    def appellate_fee_status(self) -> str:
        """Appellate fee status."""
        return self._data.get('appellate_fee_status', None)
    
    @property
    def appellate_case_type_information(self) -> str:
        """Appellate case type information."""
        return self._data.get('appellate_case_type_information', None)
    
    @property
    def mdl_status(self) -> str:
        """MDL status."""
        return self._data.get('mdl_status', None)
    
    @property
    def filepath_local(self) -> str:
        """Local file path."""
        return self._data.get('filepath_local', None)
    
    @property
    def filepath_ia(self) -> str:
        """Internet Archive file path."""
        return self._data.get('filepath_ia', None)
    
    @property
    def filepath_ia_json(self) -> str:
        """Internet Archive JSON file path."""
        return self._data.get('filepath_ia_json', None)
    
    @property
    def ia_upload_failure_count(self) -> int:
        """Number of IA upload failures."""
        return self._data.get('ia_upload_failure_count', 0)
    
    @property
    def ia_needs_upload(self) -> bool:
        """Whether IA upload is needed."""
        return self._data.get('ia_needs_upload', False)
    
    @property
    def ia_date_first_good_file(self) -> Optional[date]:
        """Date of first good IA file."""
        date_str = self._data.get('ia_date_first_good_file', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def ia_date_last_good_file(self) -> Optional[date]:
        """Date of last good IA file."""
        date_str = self._data.get('ia_date_last_good_file', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def blocked(self) -> bool:
        """Whether the docket is blocked."""
        return self._data.get('blocked', False)
    
    @property
    def blocked_reason(self) -> str:
        """Reason for blocking."""
        return self._data.get('blocked_reason', None)
    
    @property
    def date_blocked(self) -> Optional[date]:
        """Date when docket was blocked."""
        date_str = self._data.get('date_blocked', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def appeal_from_str(self) -> str:
        """Appeal from string."""
        return self._data.get('appeal_from_str', None)
    
    @property
    def assigned_to_str(self) -> str:
        """Assigned to string."""
        return self._data.get('assigned_to_str', None)
    
    @property
    def referred_to_str(self) -> str:
        """Referred to string."""
        return self._data.get('referred_to_str', None)
    
    @property
    def panel_str(self) -> str:
        """Panel string."""
        return self._data.get('panel_str', None)
    
    @property
    def date_cert_granted(self) -> Optional[date]:
        """Date when cert was granted."""
        date_str = self._data.get('date_cert_granted', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_cert_denied(self) -> Optional[date]:
        """Date when cert was denied."""
        date_str = self._data.get('date_cert_denied', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_argued(self) -> Optional[date]:
        """Date when case was argued."""
        date_str = self._data.get('date_argued', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_reargued(self) -> Optional[date]:
        """Date when case was reargued."""
        date_str = self._data.get('date_reargued', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_reargument_denied(self) -> Optional[date]:
        """Date when reargument was denied."""
        date_str = self._data.get('date_reargument_denied', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the docket."""
        return self._data.get('resource_uri', None)
    
    @property
    def is_terminated(self) -> bool:
        """Check if docket is terminated."""
        return bool(self._data.get('date_terminated') or self._data.get('terminated'))
    
    @property
    def has_audio(self) -> bool:
        """Check if docket has audio."""
        audio_count = self._data.get('audio_count', 0)
        return bool(audio_count and audio_count > 0)
    
    @property
    def has_opinions(self) -> bool:
        """Check if docket has opinions."""
        opinion_count = self._data.get('opinion_count', 0)
        return bool(opinion_count and opinion_count > 0)
    
    @property
    def has_recap(self) -> bool:
        """Check if docket has RECAP documents."""
        recap_count = self._data.get('recap_documents_count', 0)
        return bool(recap_count and recap_count > 0)
    
    def __repr__(self) -> str:
        """String representation of the docket."""
        return f"Docket(id={self.docket_id}, case_name='{self.case_name}')"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'docket_id'):
            docket_number = self._data.get('docket_number', 'None')
            case_name = self._data.get('case_name', 'None')
            return f"Docket(id={self.docket_id}, docket_number='{docket_number}', case_name='{case_name}')"
        return f"{class_name}()" 