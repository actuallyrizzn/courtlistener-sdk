"""
Position model for CourtListener SDK.

This model represents a judicial position, which is an appointment or role
of a judge in a court.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from .base import BaseModel


class Position(BaseModel):
    """Model representing a judicial position."""
    
    def __init__(self, **kwargs):
        """Initialize a Position instance.
        
        Args:
            **kwargs: Position data from the API
        """
        self.id = kwargs.get('id')
        self.judge = kwargs.get('judge')
        self.court = kwargs.get('court')
        self.position_type = kwargs.get('position_type')
        self.title = kwargs.get('title')
        self.date_start = self._parse_date(kwargs.get('date_start'))
        self.date_termination = self._parse_date(kwargs.get('date_termination'))
        self.date_created = self._parse_date(kwargs.get('date_created'))
        self.date_modified = self._parse_date(kwargs.get('date_modified'))
        self.supervisor = kwargs.get('supervisor')
        self.predecessor = kwargs.get('predecessor')
        self.appointer = kwargs.get('appointer')
        self.nomination_process = kwargs.get('nomination_process')
        self.vote_type = kwargs.get('vote_type')
        self.vote_yes = kwargs.get('vote_yes')
        self.vote_no = kwargs.get('vote_no')
        self.vote_other = kwargs.get('vote_other')
        self.vote_total = kwargs.get('vote_total')
        self.termination_reason = kwargs.get('termination_reason')
        self.seat = kwargs.get('seat')
        self.absolute_url = kwargs.get('absolute_url')
        self.resource_uri = kwargs.get('resource_uri')
        
        # Related objects (if included in response)
        self.judge_obj = kwargs.get('judge_obj')
        self.court_obj = kwargs.get('court_obj')
        self.supervisor_obj = kwargs.get('supervisor_obj')
        self.predecessor_obj = kwargs.get('predecessor_obj')
        self.appointer_obj = kwargs.get('appointer_obj')
    
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
    def is_active(self) -> bool:
        """Check if this position is currently active.
        
        Returns:
            True if position is active, False otherwise
        """
        return self.date_termination is None
    
    @property
    def duration_days(self) -> Optional[int]:
        """Get the duration of the position in days.
        
        Returns:
            Number of days the position lasted, or None if still active
        """
        if not self.date_start:
            return None
        if self.is_active:
            end_date = datetime.now()
        else:
            end_date = self.date_termination
        return (end_date - self.date_start).days
    
    @property
    def has_vote_data(self) -> bool:
        """Check if this position has vote data.
        
        Returns:
            True if position has vote data, False otherwise
        """
        return (self.vote_yes is not None or 
                self.vote_no is not None or 
                self.vote_other is not None)
    
    @property
    def vote_percentage(self) -> Optional[float]:
        """Get the percentage of yes votes.
        
        Returns:
            Percentage of yes votes, or None if no vote data
        """
        if not self.has_vote_data or not self.vote_total:
            return None
        return (self.vote_yes or 0) / self.vote_total * 100
    
    def get_vote_summary(self) -> Dict[str, Any]:
        """Get a summary of the vote data.
        
        Returns:
            Dictionary with vote summary information
        """
        if not self.has_vote_data:
            return {}
        
        return {
            'yes': self.vote_yes or 0,
            'no': self.vote_no or 0,
            'other': self.vote_other or 0,
            'total': self.vote_total or 0,
            'percentage_yes': self.vote_percentage,
            'vote_type': self.vote_type
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the position to a dictionary.
        
        Returns:
            Dictionary representation of the position
        """
        return {
            'id': self.id,
            'judge': self.judge,
            'court': self.court,
            'position_type': self.position_type,
            'title': self.title,
            'date_start': self.date_start.isoformat() if self.date_start else None,
            'date_termination': self.date_termination.isoformat() if self.date_termination else None,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_modified': self.date_modified.isoformat() if self.date_modified else None,
            'supervisor': self.supervisor,
            'predecessor': self.predecessor,
            'appointer': self.appointer,
            'nomination_process': self.nomination_process,
            'vote_type': self.vote_type,
            'vote_yes': self.vote_yes,
            'vote_no': self.vote_no,
            'vote_other': self.vote_other,
            'vote_total': self.vote_total,
            'termination_reason': self.termination_reason,
            'seat': self.seat,
            'absolute_url': self.absolute_url,
            'resource_uri': self.resource_uri
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Position':
        """Create a Position instance from a dictionary.
        
        Args:
            data: Dictionary containing position data
            
        Returns:
            Position instance
        """
        return cls(**data)
    
    def __str__(self) -> str:
        """String representation of the position.
        
        Returns:
            String representation
        """
        status = "Active" if self.is_active else "Terminated"
        return f"Position(id={self.id}, title='{self.title}', court={self.court}, status={status})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the position.
        
        Returns:
            Detailed string representation
        """
        return f"<Position(id={self.id}, judge={self.judge}, court={self.court}, position_type={self.position_type}, date_start={self.date_start})>" 