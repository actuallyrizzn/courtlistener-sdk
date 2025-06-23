"""
Opinion Cluster model for CourtListener SDK.

This model represents an opinion cluster, which groups related opinions
together (e.g., majority, concurring, dissenting opinions in the same case).
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import BaseModel


class OpinionCluster(BaseModel):
    """Model representing an opinion cluster."""
    
    def __init__(self, data: dict):
        """Initialize an OpinionCluster instance.
        
        Args:
            data: Dictionary containing opinion cluster data from the API
        """
        super().__init__(data)
    
    @property
    def id(self) -> int:
        """Cluster ID."""
        return self._data.get('id', None)
    
    @property
    def case_name(self) -> str:
        """Case name."""
        return self._data.get('case_name', None)
    
    @property
    def case_name_short(self) -> str:
        """Short case name."""
        return self._data.get('case_name_short', None)
    
    @property
    def case_name_full(self) -> str:
        """Full case name."""
        return self._data.get('case_name_full', None)
    
    @property
    def case_name_slug(self) -> str:
        """Case name slug."""
        return self._data.get('case_name_slug', None)
    
    @property
    def date_filed(self) -> Optional[datetime]:
        """Date when case was filed."""
        date_str = self._data.get('date_filed', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date when cluster was created."""
        date_str = self._data.get('date_created', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date when cluster was last modified."""
        date_str = self._data.get('date_modified', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def court(self) -> str:
        """Court URL."""
        return self._data.get('court', None)
    
    @property
    def docket(self) -> str:
        """Docket URL."""
        return self._data.get('docket', None)
    
    @property
    def citations(self) -> List[dict]:
        """List of citations."""
        return self._data.get('citations', [])
    
    @property
    def sub_opinions(self) -> List[dict]:
        """List of sub-opinions."""
        return self._data.get('sub_opinions', [])
    
    @property
    def absolute_url(self) -> str:
        """Absolute URL for the cluster."""
        return self._data.get('absolute_url', None)
    
    @property
    def resource_uri(self) -> str:
        """Resource URI for the cluster."""
        return self._data.get('resource_uri', None)
    
    @property
    def slug(self) -> str:
        """URL slug."""
        return self._data.get('slug', None)
    
    @property
    def lexis_cite(self) -> str:
        """Lexis citation."""
        return self._data.get('lexis_cite', None)
    
    @property
    def westlaw_cite(self) -> str:
        """Westlaw citation."""
        return self._data.get('westlaw_cite', None)
    
    @property
    def scdb_id(self) -> str:
        """Supreme Court Database ID."""
        return self._data.get('scdb_id', None)
    
    @property
    def scdb_decision_direction(self) -> str:
        """SCDB decision direction."""
        return self._data.get('scdb_decision_direction', None)
    
    @property
    def scdb_votes_majority(self) -> int:
        """SCDB majority votes."""
        return self._data.get('scdb_votes_majority', None)
    
    @property
    def scdb_votes_minority(self) -> int:
        """SCDB minority votes."""
        return self._data.get('scdb_votes_minority', None)
    
    @property
    def scdb_justice_votes(self) -> dict:
        """SCDB justice votes."""
        return self._data.get('scdb_justice_votes', {})
    
    @property
    def attorneys(self) -> List[dict]:
        """List of attorneys."""
        return self._data.get('attorneys', [])
    
    @property
    def panel(self) -> List[dict]:
        """List of panel judges."""
        return self._data.get('panel', [])
    
    @property
    def non_participating_judges(self) -> List[dict]:
        """List of non-participating judges."""
        return self._data.get('non_participating_judges', [])
    
    @property
    def citation_count(self) -> int:
        """Number of citations."""
        return self._data.get('citation_count', 0)
    
    @property
    def precedential(self) -> bool:
        """Whether the cluster is precedential."""
        return self._data.get('precedential', True)
    
    @property
    def date_blocked(self) -> Optional[datetime]:
        """Date when cluster was blocked."""
        date_str = self._data.get('date_blocked', None)
        return self._parse_datetime(date_str) if date_str else None
    
    @property
    def blocked(self) -> bool:
        """Whether the cluster is blocked."""
        return self._data.get('blocked', False)
    
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
    def has_citations(self) -> bool:
        """Check if this cluster has citations.
        
        Returns:
            True if cluster has citations, False otherwise
        """
        return bool(self.citations) or self.citation_count > 0
    
    @property
    def is_precedential(self) -> bool:
        """Check if this cluster is precedential.
        
        Returns:
            True if cluster is precedential, False otherwise
        """
        return self.precedential
    
    @property
    def is_blocked(self) -> bool:
        """Check if this cluster is blocked.
        
        Returns:
            True if cluster is blocked, False otherwise
        """
        return self.blocked
    
    @property
    def has_scdb_data(self) -> bool:
        """Check if this cluster has SCDB (Supreme Court Database) data.
        
        Returns:
            True if cluster has SCDB data, False otherwise
        """
        return bool(self.scdb_id)
    
    def get_majority_opinion(self) -> Optional[Dict[str, Any]]:
        """Get the majority opinion from the cluster.
        
        Returns:
            Majority opinion data or None if not found
        """
        for opinion in self.sub_opinions:
            if opinion.get('type') == '010combined':
                return opinion
        return None
    
    def get_concurring_opinions(self) -> List[Dict[str, Any]]:
        """Get all concurring opinions from the cluster.
        
        Returns:
            List of concurring opinion data
        """
        return [op for op in self.sub_opinions if op.get('type') == '020concurring']
    
    def get_dissenting_opinions(self) -> List[Dict[str, Any]]:
        """Get all dissenting opinions from the cluster.
        
        Returns:
            List of dissenting opinion data
        """
        return [op for op in self.sub_opinions if op.get('type') == '030dissenting']
    
    def get_citation_texts(self) -> List[str]:
        """Get list of citation texts.
        
        Returns:
            List of citation strings
        """
        return [cite.get('cite', '') for cite in self.citations if cite.get('cite')]
    
    def get_judge_names(self) -> List[str]:
        """Get list of judge names from the panel.
        
        Returns:
            List of judge names
        """
        return [judge.get('name', '') for judge in self.panel if judge.get('name')]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the opinion cluster to a dictionary.
        
        Returns:
            Dictionary representation of the opinion cluster
        """
        return {
            'id': self.id,
            'case_name': self.case_name,
            'case_name_short': self.case_name_short,
            'case_name_full': self.case_name_full,
            'case_name_slug': self.case_name_slug,
            'date_filed': self.date_filed.isoformat() if self.date_filed else None,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'court': self.court,
            'docket': self.docket,
            'citations': self.citations,
            'sub_opinions': self.sub_opinions,
            'absolute_url': self.absolute_url,
            'resource_uri': self.resource_uri,
            'slug': self.slug,
            'lexis_cite': self.lexis_cite,
            'westlaw_cite': self.westlaw_cite,
            'scdb_id': self.scdb_id,
            'scdb_decision_direction': self.scdb_decision_direction,
            'scdb_votes_majority': self.scdb_votes_majority,
            'scdb_votes_minority': self.scdb_votes_minority,
            'scdb_justice_votes': self.scdb_justice_votes,
            'attorneys': self.attorneys,
            'panel': self.panel,
            'non_participating_judges': self.non_participating_judges,
            'citation_count': self.citation_count,
            'precedential': self.precedential,
            'date_blocked': self.date_blocked.isoformat() if self.date_blocked else None,
            'blocked': self.blocked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OpinionCluster':
        """Create an OpinionCluster instance from a dictionary.
        
        Args:
            data: Dictionary containing opinion cluster data
            
        Returns:
            OpinionCluster instance
        """
        return cls(data)
    
    def __str__(self) -> str:
        """String representation of the opinion cluster.
        
        Returns:
            String representation
        """
        return f"OpinionCluster(id={self.id}, case_name='{self.case_name_short or self.case_name}')"
    
    def __repr__(self) -> str:
        """Detailed string representation of the opinion cluster.
        
        Returns:
            Detailed string representation
        """
        return f"<OpinionCluster(id={self.id}, case_name='{self.case_name}', court={self.court}, date_filed={self.date_filed})>" 