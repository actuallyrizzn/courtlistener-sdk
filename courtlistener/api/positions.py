"""
Positions API module for CourtListener SDK.

This module provides access to judicial positions, which represent the
appointments and roles of judges in courts.
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from ..models.position import Position
from ..utils.filters import build_filters

if TYPE_CHECKING:
    from ..client import CourtListenerClient


class PositionsAPI:
    """API client for positions endpoints."""
    
    def __init__(self, client: 'CourtListenerClient'):
        """Initialize the Positions API client.
        
        Args:
            client: The main CourtListener client instance
        """
        self.client = client
        self.base_url = "/api/rest/v4/positions/"
    
    def list_positions(self, filters: Optional[Dict[str, Any]] = None,
                      limit: Optional[int] = None) -> List[Position]:
        """List judicial positions with optional filtering.
        
        Args:
            filters: Optional dictionary of filters to apply
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        params = {}
        
        if filters:
            params.update(build_filters(filters))
            
        if limit:
            params['limit'] = limit
            
        response = self.client.get(self.base_url, params=params)
        return [Position.from_dict(position) for position in response.get('results', [])]
    
    def get_position(self, position_id: int) -> Position:
        """Get a specific judicial position by ID.
        
        Args:
            position_id: The ID of the position to retrieve
            
        Returns:
            Position object
            
        Raises:
            NotFoundError: If the position is not found
            CourtListenerError: If the API request fails
        """
        url = f"{self.base_url}{position_id}/"
        response = self.client.get(url)
        return Position.from_dict(response)
    
    def get_positions_by_judge(self, judge_id: int,
                              limit: Optional[int] = None) -> List[Position]:
        """Get positions for a specific judge.
        
        Args:
            judge_id: The judge ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'judge': judge_id}
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_court(self, court_id: int,
                              limit: Optional[int] = None) -> List[Position]:
        """Get positions for a specific court.
        
        Args:
            court_id: The court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'court': court_id}
        return self.list_positions(filters=filters, limit=limit)
    
    def get_active_positions(self, court_id: Optional[int] = None,
                           limit: Optional[int] = None) -> List[Position]:
        """Get currently active positions.
        
        Args:
            court_id: Optional court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'date_termination__isnull': True}
        if court_id:
            filters['court'] = court_id
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_position_type(self, position_type: str,
                                     court_id: Optional[int] = None,
                                     limit: Optional[int] = None) -> List[Position]:
        """Get positions by position type.
        
        Args:
            position_type: The position type to filter by (e.g., "jud", "mag")
            court_id: Optional court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'position_type': position_type}
        if court_id:
            filters['court'] = court_id
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_date_range(self, start_date: str,
                                   end_date: str,
                                   court_id: Optional[int] = None,
                                   limit: Optional[int] = None) -> List[Position]:
        """Get positions within a date range (based on start date).
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            court_id: Optional court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'date_start__gte': start_date,
            'date_start__lte': end_date
        }
        if court_id:
            filters['court'] = court_id
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_nomination_process(self, nomination_process: str,
                                          limit: Optional[int] = None) -> List[Position]:
        """Get positions by nomination process.
        
        Args:
            nomination_process: The nomination process to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'nomination_process': nomination_process}
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_supervisor(self, supervisor_id: int,
                                  limit: Optional[int] = None) -> List[Position]:
        """Get positions supervised by a specific judge.
        
        Args:
            supervisor_id: The supervisor judge ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'supervisor': supervisor_id}
        return self.list_positions(filters=filters, limit=limit)
    
    def get_positions_by_jurisdiction(self, jurisdiction: str,
                                    limit: Optional[int] = None) -> List[Position]:
        """Get positions by jurisdiction.
        
        Args:
            jurisdiction: The jurisdiction to filter by (e.g., "F", "S", "C")
            limit: Optional limit on number of results
            
        Returns:
            List of Position objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'court__jurisdiction': jurisdiction}
        return self.list_positions(filters=filters, limit=limit)
    
    def get_current_position_for_judge(self, judge_id: int) -> Optional[Position]:
        """Get the current active position for a judge.
        
        Args:
            judge_id: The judge ID to get the current position for
            
        Returns:
            Position object if found, None otherwise
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'judge': judge_id,
            'date_termination__isnull': True
        }
        positions = self.list_positions(filters=filters, limit=1)
        return positions[0] if positions else None 