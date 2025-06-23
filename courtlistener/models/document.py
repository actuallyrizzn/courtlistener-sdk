"""Document model for CourtListener SDK."""

from .base import BaseModel


class Document(BaseModel):
    """Model for document data."""
    
    def _parse_data(self):
        """Parse document data."""
        super()._parse_data()
        
        # Map API fields to expected properties
        if hasattr(self, 'docket_entry') and not hasattr(self, 'docket'):
            # Extract docket from docket_entry if possible
            self.docket = None
        elif not hasattr(self, 'docket'):
            self.docket = None
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed)
    
    @property
    def has_local_file(self) -> bool:
        """Check if document has a local file."""
        return bool(
            getattr(self, 'local_path', None) or 
            getattr(self, 'file_path', None) or
            getattr(self, 'file_url', None)
        )
    
    @property
    def docket_entry(self) -> int:
        """Get docket entry ID."""
        return getattr(self, 'docket_entry_id', None)
    
    def __repr__(self) -> str:
        """String representation of the document."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            document_number = getattr(self, 'document_number', 'Unknown')
            document_type = getattr(self, 'document_type', getattr(self, 'type', 'Unknown'))
            description = getattr(self, 'description', 'Unknown')
            return f"{class_name}(id={self.id}, document_number='{document_number}', document_type='{document_type}', description='{description}')"
        return f"{class_name}()" 