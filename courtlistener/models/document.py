"""Document model for CourtListener SDK."""

from .base import BaseModel


class Document(BaseModel):
    """Model for document data."""
    
    def _parse_data(self):
        """Parse document data."""
        super()._parse_data()
        for field in [
            'id', 'docket', 'docket_entry', 'document_number', 'document_type', 'type', 'description',
            'local_path', 'file_path', 'file_url', 'filepath_local', 'date_filed', 'absolute_url', 'resource_uri']:
            if not hasattr(self, field):
                setattr(self, field, None)
        
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
        return bool(self.local_path or self.file_path or self.file_url or self.filepath_local)
    
    @property
    def docket_entry(self) -> int:
        """Get docket entry ID."""
        return getattr(self, '_docket_entry', None)
    
    @property
    def has_ia_file(self) -> bool:
        return self.has_local_file
    
    def __repr__(self) -> str:
        """String representation of the document."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket = getattr(self, 'docket', None)
            document_number = getattr(self, 'document_number', 'None')
            document_type = getattr(self, 'document_type', getattr(self, 'type', 'None'))
            return f"<Document(id={self.id}, docket={docket}, document_number='{document_number}', document_type='{document_type}')>"
        return f"<Document()>"
    
    def __str__(self) -> str:
        """String representation of the document."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            document_number = getattr(self, 'document_number', 'None')
            document_type = getattr(self, 'document_type', getattr(self, 'type', 'None'))
            description = getattr(self, 'description', 'None')
            return f"Document(id={self.id}, document_number='{document_number}', document_type='{document_type}', description='{description}')"
        return f"{class_name}()" 