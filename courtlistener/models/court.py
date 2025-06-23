"""Court model for CourtListener SDK."""

from typing import Optional, List
from datetime import datetime, date
from .base import BaseModel


class Court(BaseModel):
    """Model for court data."""
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    @property
    def id(self) -> str:
        """Court ID."""
        return self._data.get('id', None)
    
    @property
    def name(self) -> str:
        """Court name (using short_name from API)."""
        return self._data.get('short_name', None)
    
    @property
    def full_name(self) -> str:
        """Full court name."""
        return self._data.get('full_name', None)
    
    @property
    def citation_string(self) -> str:
        """Citation string for the court."""
        return self._data.get('citation_string', None)
    
    @property
    def url(self) -> str:
        """Court URL."""
        return self._data.get('url', None)
    
    @property
    def jurisdiction(self) -> str:
        """Court jurisdiction."""
        return self._data.get('jurisdiction', None)
    
    @property
    def start_date(self) -> Optional[date]:
        """Court start date."""
        start_date_val = self._data.get('start_date', None)
        if start_date_val is None:
            return None
        elif isinstance(start_date_val, date) and not isinstance(start_date_val, datetime):
            return start_date_val
        elif isinstance(start_date_val, datetime):
            return start_date_val.date()
        elif isinstance(start_date_val, str):
            try:
                return self._parse_date(start_date_val)
            except:
                try:
                    # Try parsing as datetime first
                    dt = self._parse_datetime(start_date_val)
                    return dt.date() if dt else None
                except:
                    return None
        else:
            # Handle any other type by converting to string first
            try:
                return self._parse_date(str(start_date_val))
            except:
                return None
    
    @property
    def end_date(self) -> Optional[date]:
        """Court end date."""
        end_date_val = self._data.get('end_date', None)
        if end_date_val is None:
            return None
        elif isinstance(end_date_val, date) and not isinstance(end_date_val, datetime):
            return end_date_val
        elif isinstance(end_date_val, datetime):
            return end_date_val.date()
        elif isinstance(end_date_val, str):
            try:
                return self._parse_date(end_date_val)
            except:
                try:
                    # Try parsing as datetime first
                    dt = self._parse_datetime(end_date_val)
                    return dt.date() if dt else None
                except:
                    return None
        else:
            # Handle any other type by converting to string first
            try:
                return self._parse_date(str(end_date_val))
            except:
                return None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when court was last modified."""
        date_str = self._data.get('date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def in_use(self) -> bool:
        """Whether the court is currently in use."""
        return self._data.get('in_use', False)
    
    @property
    def has_opinion_scraper(self) -> bool:
        """Whether the court has an opinion scraper."""
        return self._data.get('has_opinion_scraper', False)
    
    @property
    def has_oral_argument_scraper(self) -> bool:
        """Whether the court has an oral argument scraper."""
        return self._data.get('has_oral_argument_scraper', False)
    
    @property
    def pacer_court_id(self) -> Optional[str]:
        """PACER court ID."""
        return self._data.get('pacer_court_id', None)
    
    @property
    def fjc_court_id(self) -> str:
        """Federal Judicial Center court ID."""
        return self._data.get('fjc_court_id', None)
    
    @property
    def parent_court(self) -> Optional[str]:
        """Parent court URL."""
        return self._data.get('parent_court', None)
    
    @property
    def appeals_to(self) -> Optional[str]:
        """Court this court appeals to."""
        return self._data.get('appeals_to', None)
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the court."""
        return self._data.get('resource_uri', None)
    
    def __repr__(self) -> str:
        """String representation of the court."""
        return f"Court(id='{self.id}', name='{self.name}')"
    
    def _parse_data(self):
        """Parse court data."""
        super()._parse_data()
        
        # Map API fields to expected properties
        if hasattr(self, 'full_name') and not hasattr(self, 'name'):
            self.name = self.full_name
        elif not hasattr(self, 'name'):
            self.name = None
    
    @property
    def is_defunct(self) -> bool:
        """Check if court is defunct."""
        return bool(self.end_date or self.defunct)
    
    @property
    def short_name(self) -> str:
        """Get short name of the court."""
        return getattr(self, '_short_name', None) or getattr(self, 'name_abbreviation', None)
    
    def __str__(self) -> str:
        """String representation of the court."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            short_name = self.short_name
            return f"{class_name}(id={self.id}, name='{name}', short_name='{short_name}')"
        return f"{class_name}()" 