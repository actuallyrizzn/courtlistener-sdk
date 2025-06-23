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
        
        for field in [
            'id', 'docket_number', 'case_name', 'date_filed', 'date_terminated', 'terminated', 'court',
            'absolute_url', 'resource_uri']:
            if not hasattr(self, field):
                setattr(self, field, None)
    
    @property
    def is_terminated(self) -> bool:
        """Check if docket is terminated."""
        return bool(self.date_terminated or self.terminated)
    
    def __repr__(self) -> str:
        """String representation of the docket."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket_number = getattr(self, 'docket_number', 'None')
            court = getattr(self, 'court', None)
            date_filed = getattr(self, 'date_filed', None)
            return f"<Docket(id={self.id}, docket_number='{docket_number}', court={court}, date_filed={date_filed})>"
        return f"<Docket()>"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            docket_number = getattr(self, 'docket_number', 'None')
            case_name = getattr(self, 'case_name', 'None')
            return f"Docket(id={self.id}, docket_number='{docket_number}', case_name='{case_name}')"
        return f"{class_name}()" 