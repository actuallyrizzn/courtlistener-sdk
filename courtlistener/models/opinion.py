"""Opinion model for CourtListener SDK."""

from .base import BaseModel


class Opinion(BaseModel):
    """Model for opinion data."""
    
    def _parse_data(self):
        """Parse opinion data."""
        super()._parse_data()
        
        # Parse dates
        if hasattr(self, 'date_filed'):
            self.date_filed = self._parse_date(self.date_filed)
        
        # Map API fields to expected properties
        if hasattr(self, 'cluster_id') and not hasattr(self, 'cluster'):
            self.cluster = self.cluster_id
        elif not hasattr(self, 'cluster'):
            self.cluster = None
        
        for field in [
            'id', 'cluster', 'author', 'type', 'type_name', 'date_filed', 'court', 'absolute_url', 'resource_uri', 'joined_by']:
            if not hasattr(self, field):
                if field == 'joined_by':
                    setattr(self, field, [])
                else:
                    setattr(self, field, None)
    
    @property
    def author(self) -> str:
        """Get opinion author."""
        return getattr(self, '_author', None)
    
    @property
    def is_majority_opinion(self) -> bool:
        """Check if this is a majority opinion."""
        opinion_type = (self.type or '').lower()
        return opinion_type in ['majority', '010combined', 'combined']
    
    @property
    def is_concurring_opinion(self) -> bool:
        """Check if this is a concurring opinion."""
        opinion_type = (self.type or '').lower()
        return opinion_type in ['concurrence', 'concurring', '020concurring']
    
    def __repr__(self) -> str:
        """String representation of the opinion."""
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            cluster = getattr(self, 'cluster', None)
            author = getattr(self, 'author', None)
            opinion_type = getattr(self, 'type', 'Unknown')
            return f"<Opinion(id={self.id}, cluster={cluster}, author={author}, type='{opinion_type}')>"
        return f"<Opinion()>"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            opinion_type = getattr(self, 'type', 'Unknown')
            type_name = getattr(self, 'type_name', 'Unknown')
            return f"{class_name}(id={self.id}, type='{opinion_type}', type_name='{type_name}')"
        return f"{class_name}()" 