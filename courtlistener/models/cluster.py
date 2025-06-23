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
    
    def __init__(self, **kwargs):
        """Initialize an OpinionCluster instance.
        
        Args:
            **kwargs: Opinion cluster data from the API
        """
        self.id = kwargs.get('id')
        self.case_name = kwargs.get('case_name')
        self.case_name_short = kwargs.get('case_name_short')
        self.case_name_full = kwargs.get('case_name_full')
        self.case_name_slug = kwargs.get('case_name_slug')
        self.date_filed = self._parse_date(kwargs.get('date_filed'))
        self.date_created = self._parse_date(kwargs.get('date_created'))
        self.date_modified = self._parse_date(kwargs.get('date_modified'))
        self.court = kwargs.get('court')
        self.docket = kwargs.get('docket')
        self.citations = kwargs.get('citations', [])
        self.sub_opinions = kwargs.get('sub_opinions', [])
        self.absolute_url = kwargs.get('absolute_url')
        self.resource_uri = kwargs.get('resource_uri')
        self.slug = kwargs.get('slug')
        self.lexis_cite = kwargs.get('lexis_cite')
        self.westlaw_cite = kwargs.get('westlaw_cite')
        self.scdb_id = kwargs.get('scdb_id')
        self.scdb_decision_direction = kwargs.get('scdb_decision_direction')
        self.scdb_votes_majority = kwargs.get('scdb_votes_majority')
        self.scdb_votes_minority = kwargs.get('scdb_votes_minority')
        self.scdb_justice_votes = kwargs.get('scdb_justice_votes', {})
        self.attorneys = kwargs.get('attorneys', [])
        self.panel = kwargs.get('panel', [])
        self.non_participating_judges = kwargs.get('non_participating_judges', [])
        self.citation_count = kwargs.get('citation_count', 0)
        self.precedential = kwargs.get('precedential', True)
        self.date_blocked = self._parse_date(kwargs.get('date_blocked'))
        self.blocked = kwargs.get('blocked', False)
        
        # Related objects (if included in response)
        self.court_obj = kwargs.get('court_obj')
        self.docket_obj = kwargs.get('docket_obj')
        self.citations_objs = kwargs.get('citations_objs', [])
        self.sub_opinions_objs = kwargs.get('sub_opinions_objs', [])
        self.attorneys_objs = kwargs.get('attorneys_objs', [])
        self.panel_objs = kwargs.get('panel_objs', [])
        self.non_participating_judges_objs = kwargs.get('non_participating_judges_objs', [])
    
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
        return cls(**data)
    
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