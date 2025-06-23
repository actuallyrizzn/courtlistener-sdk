"""Opinion model for CourtListener SDK."""

from typing import Optional, List
from datetime import datetime, date
from .base import BaseModel


class Opinion(BaseModel):
    """Model for opinion data."""
    
    def __init__(self, data: dict):
        super().__init__(data)
    
    @property
    def id(self) -> int:
        """Opinion ID."""
        return getattr(self, 'id', None)
    
    @property
    def case_name(self) -> str:
        """Case name (from cluster)."""
        # Try to get case name from cluster data if available
        case_name = self._data.get('case_name', None)
        if case_name:
            return case_name
        
        # Fallback: try to extract from cluster URL or use a default
        cluster_url = self._data.get('cluster', None)
        if cluster_url:
            # Extract case name from URL slug if possible
            try:
                # URL format: /opinion/10615173/churchill-house-lp-v-marshall/
                parts = cluster_url.split('/')
                if len(parts) > 2:
                    slug = parts[-2]  # Get the slug part
                    # Convert slug to readable case name
                    case_name = slug.replace('-', ' ').replace('_', ' ').title()
                    return case_name
            except:
                pass
        
        return "Unknown Case"
    
    @property
    def cluster_id(self) -> int:
        """Cluster ID."""
        return getattr(self, 'cluster_id', None)
    
    @property
    def cluster(self) -> str:
        """Cluster URL."""
        return getattr(self, 'cluster', None)
    
    @property
    def author_id(self) -> Optional[int]:
        """Author ID."""
        return getattr(self, 'author_id', None)
    
    @property
    def author(self) -> Optional[str]:
        """Author URL."""
        return getattr(self, 'author', None)
    
    @property
    def author_str(self) -> str:
        """Author string."""
        return getattr(self, 'author_str', None)
    
    @property
    def joined_by(self) -> List[str]:
        """List of judges who joined this opinion."""
        return getattr(self, 'joined_by', [])
    
    @property
    def joined_by_str(self) -> str:
        """Joined by string."""
        return getattr(self, 'joined_by_str', None)
    
    @property
    def type(self) -> str:
        """Opinion type."""
        return getattr(self, 'type', None)
    
    @property
    def per_curiam(self) -> bool:
        """Whether this is a per curiam opinion."""
        return getattr(self, 'per_curiam', False)
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when opinion was created."""
        date_str = getattr(self, 'date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when opinion was last modified."""
        date_str = getattr(self, 'date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def absolute_url(self) -> str:
        """Absolute URL for the opinion."""
        return getattr(self, 'absolute_url', None)
    
    @property
    def download_url(self) -> str:
        """Download URL for the opinion."""
        return getattr(self, 'download_url', None)
    
    @property
    def local_path(self) -> str:
        """Local path for the opinion."""
        return getattr(self, 'local_path', None)
    
    @property
    def plain_text(self) -> str:
        """Plain text content."""
        return getattr(self, 'plain_text', None)
    
    @property
    def html(self) -> str:
        """HTML content."""
        return getattr(self, 'html', None)
    
    @property
    def html_lawbox(self) -> str:
        """Lawbox HTML content."""
        return getattr(self, 'html_lawbox', None)
    
    @property
    def html_columbia(self) -> str:
        """Columbia HTML content."""
        return getattr(self, 'html_columbia', None)
    
    @property
    def html_anon_2020(self) -> str:
        """Anonymous 2020 HTML content."""
        return getattr(self, 'html_anon_2020', None)
    
    @property
    def xml_harvard(self) -> str:
        """Harvard XML content."""
        return getattr(self, 'xml_harvard', None)
    
    @property
    def html_with_citations(self) -> str:
        """HTML with citations."""
        return getattr(self, 'html_with_citations', None)
    
    @property
    def sha1(self) -> str:
        """SHA1 hash of the opinion."""
        return getattr(self, 'sha1', None)
    
    @property
    def page_count(self) -> Optional[int]:
        """Number of pages."""
        return getattr(self, 'page_count', None)
    
    @property
    def extracted_by_ocr(self) -> bool:
        """Whether the text was extracted by OCR."""
        return getattr(self, 'extracted_by_ocr', False)
    
    @property
    def ordering_key(self) -> Optional[int]:
        """Ordering key."""
        return getattr(self, 'ordering_key', None)
    
    @property
    def opinions_cited(self) -> List[str]:
        """List of cited opinion URLs."""
        return getattr(self, 'opinions_cited', [])
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the opinion."""
        return getattr(self, 'resource_uri', None)
    
    def __repr__(self) -> str:
        """String representation of the opinion."""
        return f"Opinion(id={self.id}, author='{self.author_str}')"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if hasattr(self, 'id'):
            opinion_type = getattr(self, 'type', 'Unknown')
            type_name = getattr(self, 'type_name', 'Unknown')
            return f"{class_name}(id={self.id}, type='{opinion_type}', type_name='{type_name}')"
        return f"{class_name}()" 