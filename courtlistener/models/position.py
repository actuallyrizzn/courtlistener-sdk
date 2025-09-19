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
    
    def __init__(self, data: dict):
        """Initialize a Position instance.
        
        Args:
            data: Position data from the API
        """
        super().__init__(data)
    
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
    def id(self) -> Optional[int]:
        """Position ID."""
        return self._data.get('id')
    
    @property
    def judge(self) -> Optional[str]:
        """Judge URL."""
        return self._data.get('judge')
    
    @property
    def court(self) -> Optional[str]:
        """Court URL."""
        return self._data.get('court')
    
    @property
    def position_type(self) -> Optional[str]:
        """Position type."""
        return self._data.get('position_type')
    
    @property
    def title(self) -> Optional[str]:
        """Position title."""
        return self._data.get('title')
    
    @property
    def date_start(self) -> Optional[datetime]:
        """Start date."""
        date_str = self._data.get('date_start')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_termination(self) -> Optional[datetime]:
        """Termination date."""
        date_str = self._data.get('date_termination')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_created(self) -> Optional[datetime]:
        """Date created."""
        date_str = self._data.get('date_created')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def date_modified(self) -> Optional[datetime]:
        """Date modified."""
        date_str = self._data.get('date_modified')
        return self._parse_date(date_str) if date_str else None
    
    @property
    def supervisor(self) -> Optional[str]:
        """Supervisor URL."""
        return self._data.get('supervisor')
    
    @property
    def predecessor(self) -> Optional[str]:
        """Predecessor URL."""
        return self._data.get('predecessor')
    
    @property
    def appointer(self) -> Optional[str]:
        """Appointer URL."""
        return self._data.get('appointer')
    
    @property
    def nomination_process(self) -> Optional[str]:
        """Nomination process."""
        return self._data.get('nomination_process')
    
    @property
    def vote_type(self) -> Optional[str]:
        """Vote type."""
        return self._data.get('vote_type')
    
    @property
    def vote_yes(self) -> Optional[int]:
        """Yes votes."""
        return self._data.get('vote_yes')
    
    @property
    def vote_no(self) -> Optional[int]:
        """No votes."""
        return self._data.get('vote_no')
    
    @property
    def vote_other(self) -> Optional[int]:
        """Other votes."""
        return self._data.get('vote_other')
    
    @property
    def vote_total(self) -> Optional[int]:
        """Total votes."""
        return self._data.get('vote_total')
    
    @property
    def termination_reason(self) -> Optional[str]:
        """Termination reason."""
        return self._data.get('termination_reason')
    
    @property
    def seat(self) -> Optional[str]:
        """Seat information."""
        return self._data.get('seat')
    
    @property
    def absolute_url(self) -> Optional[str]:
        """Absolute URL."""
        return self._data.get('absolute_url')
    
    @property
    def resource_uri(self) -> Optional[str]:
        """Resource URI."""
        return self._data.get('resource_uri')
    
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
    
    @property
    def is_current(self) -> bool:
        """Check if position is current."""
        return bool(getattr(self, 'date_end', None) is None)
    
    @property
    def has_end_date(self) -> bool:
        """Check if position has end date."""
        return bool(getattr(self, 'date_end', None) is not None) 