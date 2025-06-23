"""Docket model for CourtListener SDK."""

from .base import BaseModel


class Docket(BaseModel):
    """Model for docket data."""
    
    def _parse_data(self):
        """Parse docket data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_datetime(self.date_filed)
        if hasattr(self, 'date_terminated'):
            self.date_terminated = self._parse_datetime(self.date_terminated)
        
        # Map API fields to expected properties
        if hasattr(self, 'case_name') and not hasattr(self, 'case_name'):
            pass  # Already exists
        elif not hasattr(self, 'case_name'):
            self.case_name = None
        
        # Parse related models if they exist
        if hasattr(self, 'court') and isinstance(self.court, dict):
            from .court import Court
            self.court = self._parse_related_model(self.court, Court)
    
    @property
    def is_terminated(self) -> bool:
        """Check if docket is terminated."""
        return bool(
            getattr(self, 'date_terminated', None) or
            getattr(self, 'terminated', False) or
            self._data.get('is_terminated', False)
        )
    
    def __repr__(self) -> str:
        """String representation of the docket."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket_number = getattr(self, 'docket_number', 'Unknown')
            case_name = getattr(self, 'case_name', 'Unknown')
            return f"{class_name}(id={self.id}, docket_number='{docket_number}', case_name='{case_name}')"
        return f"{class_name}()" 