"""
Docket Entry model for CourtListener SDK.

This model represents a docket entry, which is an individual filing or event
within a docket.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import BaseModel


class DocketEntry(BaseModel):
    """Model representing a docket entry."""
    
    def __init__(self, data: dict):
        """Initialize a DocketEntry instance.
        
        Args:
            data: Docket entry data from the API
        """
        super().__init__(data)
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object.
        
        Args:
            date_str: Date string from API
            
        Returns:
            Parsed datetime object or None
        """
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    @property
    def id(self) -> Optional[int]:
        """Docket entry ID."""
        return self._data.get('id')
    
    @property
    def docket(self) -> Optional[str]:
        """Docket URL."""
        return self._data.get('docket')
    
    @property
    def entry_number(self) -> Optional[int]:
        """Entry number."""
        return self._data.get('entry_number')
    
    @property
    def description(self) -> Optional[str]:
        """Entry description."""
        return self._data.get('description')
    
    @property
    def date_filed(self) -> Optional[datetime]:
        """Date filed."""
        date_str = self._data.get('date_filed')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date created."""
        date_str = self._data.get('date_created')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date modified."""
        date_str = self._data.get('date_modified')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def recap_documents(self) -> List[str]:
        """List of RECAP document URLs."""
        return self._data.get('recap_documents', [])
    
    @property
    def seal(self) -> bool:
        """Whether entry is sealed."""
        return self._data.get('seal', False)
    
    @property
    def sealed_date(self) -> Optional[datetime]:
        """Sealed date."""
        date_str = self._data.get('sealed_date')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def entry_number_str(self) -> Optional[str]:
        """Entry number as string."""
        return self._data.get('entry_number_str')
    
    @property
    def description_short(self) -> Optional[str]:
        """Short description."""
        return self._data.get('description_short')
    
    @property
    def description_plain(self) -> Optional[str]:
        """Plain text description."""
        return self._data.get('description_plain')
    
    @property
    def description_html(self) -> Optional[str]:
        """HTML description."""
        return self._data.get('description_html')
    
    @property
    def recap_sequence_number(self) -> Optional[int]:
        """RECAP sequence number."""
        return self._data.get('recap_sequence_number')
    
    @property
    def recap_documents_count(self) -> int:
        """Number of RECAP documents."""
        return self._data.get('recap_documents_count', 0)
    
    @property
    def absolute_url(self) -> Optional[str]:
        """Absolute URL."""
        return self._data.get('absolute_url')
    
    @property
    def resource_uri(self) -> Optional[str]:
        """Resource URI."""
        return self._data.get('resource_uri')
    
    @property
    def has_documents(self) -> bool:
        """Check if this entry has associated documents.
        
        Returns:
            True if entry has documents, False otherwise
        """
        return bool(self.recap_documents) or self.recap_documents_count > 0
    
    @property
    def is_sealed(self) -> bool:
        """Check if this entry is sealed.
        
        Returns:
            True if entry is sealed, False otherwise
        """
        return self.seal
    
    def get_documents(self) -> List[str]:
        """Get list of document IDs associated with this entry.
        
        Returns:
            List of document resource URIs
        """
        return self.recap_documents
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the docket entry to a dictionary.
        
        Returns:
            Dictionary representation of the docket entry
        """
        return {
            'id': self.id,
            'docket': self.docket,
            'entry_number': self.entry_number,
            'description': self.description,
            'date_filed': self.date_filed.isoformat() if self.date_filed else None,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'recap_documents': self.recap_documents,
            'seal': self.seal,
            'sealed_date': self.sealed_date.isoformat() if self.sealed_date else None,
            'entry_number_str': self.entry_number_str,
            'description_short': self.description_short,
            'description_plain': self.description_plain,
            'description_html': self.description_html,
            'recap_sequence_number': self.recap_sequence_number,
            'recap_documents_count': self.recap_documents_count,
            'absolute_url': self.absolute_url,
            'resource_uri': self.resource_uri
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocketEntry':
        """Create a DocketEntry instance from a dictionary.
        
        Args:
            data: Dictionary containing docket entry data
            
        Returns:
            DocketEntry instance
        """
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation of the docket entry.
        
        Returns:
            String representation
        """
        return f"DocketEntry(id={self.id}, entry_number={self.entry_number}, description='{self.description_short or self.description}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the docket entry.
        
        Returns:
            Detailed string representation
        """
        return f"<DocketEntry(id={self.id}, docket={self.docket}, entry_number={self.entry_number}, date_filed={self.date_filed})>" 