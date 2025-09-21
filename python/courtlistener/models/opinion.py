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
        return self._data.get('id', None)
    
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
    def caseName(self) -> str:
        """Case name (camelCase for backward compatibility)."""
        return self.case_name
    
    @property
    def cluster_id(self) -> int:
        """Cluster ID."""
        return self._data.get('cluster_id', None)
    
    @property
    def cluster(self) -> str:
        """Cluster URL."""
        return self._data.get('cluster', None)
    
    @property
    def court(self) -> str:
        """Court URL."""
        return self._data.get('court', None)
    
    @property
    def date_filed(self) -> str:
        """Date the opinion was filed."""
        return self._data.get('date_filed', None)
    
    @property
    def author_id(self) -> Optional[int]:
        """Author ID."""
        return self._data.get('author_id', None)
    
    @property
    def author(self) -> Optional[str]:
        """Author URL."""
        return self._data.get('author', None)
    
    @property
    def author_str(self) -> str:
        """Author string."""
        return self._data.get('author_str', None)
    
    @property
    def joined_by(self) -> List[str]:
        """List of judges who joined this opinion."""
        return self._data.get('joined_by', [])
    
    @property
    def joined_by_str(self) -> str:
        """Joined by string."""
        return self._data.get('joined_by_str', None)
    
    @property
    def type(self) -> str:
        """Opinion type."""
        return self._data.get('type', None)
    
    @property
    def per_curiam(self) -> bool:
        """Whether this is a per curiam opinion."""
        return self._data.get('per_curiam', False)
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when opinion was created."""
        date_str = self._data.get('date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when opinion was last modified."""
        date_str = self._data.get('date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def absolute_url(self) -> str:
        """Absolute URL for the opinion."""
        return self._data.get('absolute_url', None)
    
    @property
    def download_url(self) -> str:
        """Download URL for the opinion."""
        return self._data.get('download_url', None)
    
    @property
    def local_path(self) -> str:
        """Local path for the opinion."""
        return self._data.get('local_path', None)
    
    @property
    def plain_text(self) -> str:
        """Plain text content."""
        return self._data.get('plain_text', None)
    
    @property
    def html(self) -> str:
        """HTML content."""
        return self._data.get('html', None)
    
    @property
    def html_lawbox(self) -> str:
        """Lawbox HTML content."""
        return self._data.get('html_lawbox', None)
    
    @property
    def html_columbia(self) -> str:
        """Columbia HTML content."""
        return self._data.get('html_columbia', None)
    
    @property
    def html_anon_2020(self) -> str:
        """Anonymous 2020 HTML content."""
        return self._data.get('html_anon_2020', None)
    
    @property
    def xml_harvard(self) -> str:
        """Harvard XML content."""
        return self._data.get('xml_harvard', None)
    
    @property
    def html_with_citations(self) -> str:
        """HTML with citations."""
        return self._data.get('html_with_citations', None)
    
    @property
    def sha1(self) -> str:
        """SHA1 hash of the opinion."""
        return self._data.get('sha1', None)
    
    @property
    def page_count(self) -> Optional[int]:
        """Number of pages."""
        return self._data.get('page_count', None)
    
    @property
    def extracted_by_ocr(self) -> bool:
        """Whether the text was extracted by OCR."""
        return self._data.get('extracted_by_ocr', False)
    
    @property
    def ordering_key(self) -> Optional[int]:
        """Ordering key."""
        return self._data.get('ordering_key', None)
    
    @property
    def opinions_cited(self) -> List[str]:
        """List of cited opinion URLs."""
        return self._data.get('opinions_cited', [])
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the opinion."""
        return self._data.get('resource_uri', None)
    
    def __repr__(self) -> str:
        """String representation of the opinion."""
        return f"Opinion(id={self.id}, author='{self.author_str}')"
    
    def __str__(self) -> str:
        class_name = self.__class__.__name__
        if self.id is not None:
            opinion_type = self._data.get('type', 'Unknown')
            type_name = self._data.get('type_name', 'Unknown')
            return f"{class_name}(id={self.id}, type='{opinion_type}', type_name='{type_name}')"
        return f"{class_name}()" 