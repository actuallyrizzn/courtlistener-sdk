"""
Opinion Clusters API module for CourtListener SDK.

This module provides access to opinion clusters, which group related opinions
together (e.g., majority, concurring, dissenting opinions in the same case).
"""

from typing import Dict, List, Optional, Any, TYPE_CHECKING
from ..models.cluster import OpinionCluster
from ..utils.filters import build_filters

if TYPE_CHECKING:
    from ..client import CourtListenerClient


class ClustersAPI:
    """API client for opinion clusters endpoints."""
    
    def __init__(self, client: 'CourtListenerClient'):
        """Initialize the Clusters API client.
        
        Args:
            client: The main CourtListener client instance
        """
        self.client = client
        self.base_url = "/api/rest/v4/clusters/"
    
    def list_clusters(self, filters: Optional[Dict[str, Any]] = None,
                     limit: Optional[int] = None) -> List[OpinionCluster]:
        """List opinion clusters with optional filtering.
        
        Args:
            filters: Optional dictionary of filters to apply
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        params = {}
        
        if filters:
            params.update(build_filters(**filters))
            
        if limit:
            params['limit'] = limit
            
        response = self.client.get(self.base_url, params=params)
        return [OpinionCluster.from_dict(cluster) for cluster in response.get('results', [])]
    
    def get_cluster(self, cluster_id: int) -> OpinionCluster:
        """Get a specific opinion cluster by ID.
        
        Args:
            cluster_id: The ID of the opinion cluster to retrieve
            
        Returns:
            OpinionCluster object
            
        Raises:
            NotFoundError: If the cluster is not found
            CourtListenerError: If the API request fails
        """
        url = f"{self.base_url}{cluster_id}/"
        response = self.client.get(url)
        return OpinionCluster.from_dict(response)
    
    def get_clusters_by_court(self, court_id: int,
                             filters: Optional[Dict[str, Any]] = None,
                             limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters for a specific court.
        
        Args:
            court_id: The court ID to filter by
            filters: Optional additional filters to apply
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        cluster_filters = {'court': court_id}
        if filters:
            cluster_filters.update(filters)
        return self.list_clusters(filters=cluster_filters, limit=limit)
    
    def get_cluster_by_citation(self, citation: str) -> Optional[OpinionCluster]:
        """Get an opinion cluster by citation.
        
        Args:
            citation: The citation to search for (e.g., "410 U.S. 113")
            
        Returns:
            OpinionCluster object if found, None otherwise
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'citations__cite': citation}
        clusters = self.list_clusters(filters=filters, limit=1)
        return clusters[0] if clusters else None
    
    def get_clusters_by_case_name(self, case_name: str,
                                 court_id: Optional[int] = None,
                                 limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters by case name.
        
        Args:
            case_name: The case name to search for
            court_id: Optional court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'case_name__icontains': case_name}
        if court_id:
            filters['court'] = court_id
        return self.list_clusters(filters=filters, limit=limit)
    
    def get_clusters_by_date_range(self, start_date: str,
                                  end_date: str,
                                  court_id: Optional[int] = None,
                                  limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters within a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            court_id: Optional court ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {
            'date_filed__gte': start_date,
            'date_filed__lte': end_date
        }
        if court_id:
            filters['court'] = court_id
        return self.list_clusters(filters=filters, limit=limit)
    
    def get_clusters_by_docket(self, docket_id: int) -> List[OpinionCluster]:
        """Get opinion clusters for a specific docket.
        
        Args:
            docket_id: The docket ID to filter by
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'docket': docket_id}
        return self.list_clusters(filters=filters)
    
    def get_clusters_by_judge(self, judge_id: int,
                             limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters authored by a specific judge.
        
        Args:
            judge_id: The judge ID to filter by
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'sub_opinions__author': judge_id}
        return self.list_clusters(filters=filters, limit=limit)
    
    def get_clusters_by_jurisdiction(self, jurisdiction: str,
                                   limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters by jurisdiction.
        
        Args:
            jurisdiction: The jurisdiction to filter by (e.g., "F", "S", "C")
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'court__jurisdiction': jurisdiction}
        return self.list_clusters(filters=filters, limit=limit)
    
    def get_clusters_with_citations(self, limit: Optional[int] = None) -> List[OpinionCluster]:
        """Get opinion clusters that have citations.
        
        Args:
            limit: Optional limit on number of results
            
        Returns:
            List of OpinionCluster objects
            
        Raises:
            CourtListenerError: If the API request fails
        """
        filters = {'citations__isnull': False}
        return self.list_clusters(filters=filters, limit=limit) 