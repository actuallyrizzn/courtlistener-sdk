"""Attorney model for CourtListener SDK."""

from .base import BaseModel


class Attorney(BaseModel):
    """Model for attorney data."""
    
    def _parse_data(self):
        """Parse attorney data."""
        super()._parse_data()
        # Ensure all expected fields are present
        for field in [
            'name', 'firm', 'contact', 'phone', 'fax', 'address1', 'address2', 'city', 'state', 'zip_code',
            'absolute_url', 'resource_uri']:
            if not hasattr(self, field):
                setattr(self, field, None)
        
        # Map API fields to expected properties
        if hasattr(self, 'name_first') and hasattr(self, 'name_last'):
            self.name = f"{getattr(self, 'name_first', '')} {getattr(self, 'name_last', '')}".strip()
        elif hasattr(self, 'name'):
            pass  # Already exists
        else:
            self.name = None
            
        # Map organization/law_firm to firm
        if hasattr(self, 'organization') and not hasattr(self, 'firm'):
            self.firm = self.organization
        elif hasattr(self, 'law_firm') and not hasattr(self, 'firm'):
            self.firm = self.law_firm
        elif not hasattr(self, 'firm'):
            self.firm = None
    
    @property
    def has_address(self) -> bool:
        """Check if attorney has address information."""
        return bool(
            getattr(self, 'address1', None) or getattr(self, 'address2', None) or
            getattr(self, 'city', None) or getattr(self, 'state', None) or getattr(self, 'zip_code', None)
        )
    
    @property
    def full_address(self) -> str:
        """Get formatted full address."""
        parts = []
        if self.address1:
            parts.append(self.address1)
        if self.address2:
            parts.append(self.address2)
        if self.city:
            parts.append(self.city)
        # State and zip_code should be joined with a space if both exist
        state_zip = None
        if self.state and self.zip_code:
            state_zip = f"{self.state} {self.zip_code}"
        elif self.state:
            state_zip = self.state
        elif self.zip_code:
            state_zip = self.zip_code
        if state_zip:
            parts.append(state_zip)
        # Remove empty strings
        parts = [p for p in parts if p]
        return ', '.join(parts) if parts else ''
    
    @property
    def has_phone(self) -> bool:
        """Check if attorney has phone information."""
        return bool(getattr(self, 'phone', None) or getattr(self, 'phone_number', None))
    
    @property
    def contact(self) -> str:
        """Get contact information."""
        return getattr(self, '_contact', None)
    
    def __repr__(self) -> str:
        """String representation of the attorney."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            firm = getattr(self, 'firm', 'Unknown')
            city = getattr(self, 'city', None)
            return f"<{class_name}(id={self.id}, name='{name}', firm='{firm}', city={city})>"
        return f"<{class_name}()>"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            name = getattr(self, 'name', 'Unknown')
            firm = getattr(self, 'firm', 'Unknown')
            return f"{class_name}(id={self.id}, name='{name}', firm='{firm}')"
        return f"{class_name}()" 