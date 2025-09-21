"""
Judge model for CourtListener SDK.
"""

from typing import Optional, List
from datetime import datetime, date
from .base import BaseModel


class Judge(BaseModel):
    """Model for judge/people data."""
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    @property
    def id(self) -> int:
        """Judge ID."""
        return self._data.get('id', None)
    
    @property
    def name(self) -> str:
        """Full name of the judge."""
        first = self._data.get('name_first', '')
        middle = self._data.get('name_middle', '')
        last = self._data.get('name_last', '')
        suffix = self._data.get('name_suffix', '')
        
        parts = [first, middle, last, suffix]
        return ' '.join(part for part in parts if part)
    
    @property
    def name_first(self) -> str:
        """First name."""
        return self._data.get('name_first', None)
    
    @property
    def name_middle(self) -> str:
        """Middle name."""
        return self._data.get('name_middle', None)
    
    @property
    def name_last(self) -> str:
        """Last name."""
        return self._data.get('name_last', None)
    
    @property
    def name_suffix(self) -> str:
        """Name suffix."""
        return self._data.get('name_suffix', None)
    
    @property
    def slug(self) -> str:
        """URL slug for the judge."""
        return self._data.get('slug', None)
    
    @property
    def date_dob(self) -> Optional[date]:
        """Date of birth."""
        date_str = self._data.get('date_dob', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_dod(self) -> Optional[date]:
        """Date of death."""
        date_str = self._data.get('date_dod', None)
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when record was created."""
        date_str = self._data.get('date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when record was last modified."""
        date_str = self._data.get('date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def gender(self) -> str:
        """Gender."""
        return self._data.get('gender', None)
    
    @property
    def religion(self) -> str:
        """Religion."""
        return self._data.get('religion', None)
    
    @property
    def dob_city(self) -> str:
        """City of birth."""
        return self._data.get('dob_city', None)
    
    @property
    def dob_state(self) -> str:
        """State of birth."""
        return self._data.get('dob_state', None)
    
    @property
    def dob_country(self) -> str:
        """Country of birth."""
        return self._data.get('dob_country', None)
    
    @property
    def dod_city(self) -> str:
        """City of death."""
        return self._data.get('dod_city', None)
    
    @property
    def dod_state(self) -> str:
        """State of death."""
        return self._data.get('dod_state', None)
    
    @property
    def dod_country(self) -> str:
        """Country of death."""
        return self._data.get('dod_country', None)
    
    @property
    def fjc_id(self) -> Optional[str]:
        """Federal Judicial Center ID."""
        return self._data.get('fjc_id', None)
    
    @property
    def positions(self) -> List[str]:
        """List of position URLs."""
        return self._data.get('positions', [])
    
    @property
    def educations(self) -> List[str]:
        """List of education URLs."""
        return self._data.get('educations', [])
    
    @property
    def political_affiliations(self) -> List[str]:
        """List of political affiliation URLs."""
        return self._data.get('political_affiliations', [])
    
    @property
    def aba_ratings(self) -> List[str]:
        """List of ABA rating URLs."""
        return self._data.get('aba_ratings', [])
    
    @property
    def sources(self) -> List[str]:
        """List of source URLs."""
        return self._data.get('sources', [])
    
    @property
    def race(self) -> List[str]:
        """List of race URLs."""
        return self._data.get('race', [])
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the judge."""
        return self._data.get('resource_uri', None)
    
    def __repr__(self) -> str:
        """String representation of the judge."""
        return f"Judge(id={self.id}, name='{self.name}')" 