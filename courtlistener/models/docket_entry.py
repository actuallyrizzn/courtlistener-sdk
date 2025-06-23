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
    
    def __init__(self, **kwargs):
        """Initialize a DocketEntry instance.
        
        Args:
            **kwargs: Docket entry data from the API
        """
        self.id = kwargs.get('id')
        self.docket = kwargs.get('docket')
        self.entry_number = kwargs.get('entry_number')
        self.description = kwargs.get('description')
        self.date_filed = self._parse_date(kwargs.get('date_filed'))
        self.date_created = self._parse_date(kwargs.get('date_created'))
        self.date_modified = self._parse_date(kwargs.get('date_modified'))
        self.recap_documents = kwargs.get('recap_documents', [])
        self.seal = kwargs.get('seal', False)
        self.sealed_date = self._parse_date(kwargs.get('sealed_date'))
        self.entry_number_str = kwargs.get('entry_number_str')
        self.description_short = kwargs.get('description_short')
        self.description_plain = kwargs.get('description_plain')
        self.description_html = kwargs.get('description_html')
        self.recap_sequence_number = kwargs.get('recap_sequence_number')
        self.recap_documents_count = kwargs.get('recap_documents_count', 0)
        self.absolute_url = kwargs.get('absolute_url')
        self.resource_uri = kwargs.get('resource_uri')
        
        # Related objects (if included in response)
        self.docket_obj = kwargs.get('docket_obj')
        self.recap_documents_objs = kwargs.get('recap_documents_objs', [])
    
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
    
    def get_documents(self) -> List[Dict[str, Any]]:
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