"""
Docket Alerts API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class DocketAlertsAPI(BaseAPI):
    """API for managing docket-specific alerts."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "docket-alerts/"
    
    def list(
        self,
        docket: Optional[int] = None,
        alert_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List docket alerts.
        
        Args:
            docket: Filter by docket ID
            alert_type: Filter by alert type (entry, document)
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of docket alerts
        """
        params = {}
        if docket is not None:
            params['docket'] = docket
        if alert_type is not None:
            params['alert_type'] = alert_type
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, alert_id: int) -> Dict[str, Any]:
        """
        Get a specific docket alert by ID.
        
        Args:
            alert_id: Docket alert ID
        
        Returns:
            Docket alert data
        """
        return self.client.get(f"{self.endpoint}{alert_id}/")
    
    def create(
        self,
        docket: int,
        alert_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new docket alert.
        
        Args:
            docket: Docket ID to monitor
            alert_type: Type of alert (entry, document)
            webhook_url: Webhook URL for notifications
            **kwargs: Additional parameters
        
        Returns:
            Created docket alert data
        """
        data = {'docket': docket}
        if alert_type is not None:
            data['alert_type'] = alert_type
        if webhook_url is not None:
            data['webhook_url'] = webhook_url
        
        data.update(kwargs)
        return self.client.post(self.endpoint, data=data)
    
    def update(
        self,
        alert_id: int,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing docket alert.
        
        Args:
            alert_id: Docket alert ID
            **kwargs: Fields to update
        
        Returns:
            Updated docket alert data
        """
        return self.client.post(f"{self.endpoint}{alert_id}/", data=kwargs)
    
    def delete(self, alert_id: int) -> bool:
        """
        Delete a docket alert.
        
        Args:
            alert_id: Docket alert ID
        
        Returns:
            True if successful
        """
        self.client._make_request('DELETE', f"{self.endpoint}{alert_id}/")
        return True
    
    def paginate(
        self,
        docket: Optional[int] = None,
        alert_type: Optional[str] = None,
        **kwargs
    ):
        """
        Get paginated docket alerts.
        
        Args:
            docket: Filter by docket ID
            alert_type: Filter by alert type (entry, document)
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for docket alerts
        """
        params = {}
        if docket is not None:
            params['docket'] = docket
        if alert_type is not None:
            params['alert_type'] = alert_type
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
