"""
Alerts API module for CourtListener SDK.
"""

from typing import Dict, Any, Optional, List
from .base import BaseAPI


class AlertsAPI(BaseAPI):
    """API for managing search and docket alerts."""
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "alerts/"
    
    def list(
        self,
        name: Optional[str] = None,
        alert_type: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        List alerts.
        
        Args:
            name: Filter by alert name
            alert_type: Filter by alert type (search, docket)
            **kwargs: Additional query parameters
        
        Returns:
            API response with paginated list of alerts
        """
        params = {}
        if name is not None:
            params['name'] = name
        if alert_type is not None:
            params['alert_type'] = alert_type
        
        params.update(kwargs)
        return self.client.get(self.endpoint, params=params)
    
    def get(self, alert_id: int) -> Dict[str, Any]:
        """
        Get a specific alert by ID.
        
        Args:
            alert_id: Alert ID
        
        Returns:
            Alert data
        """
        return self.client.get(f"{self.endpoint}{alert_id}/")
    
    def create(
        self,
        name: str,
        query: str,
        rate: str,
        alert_type: Optional[str] = None,
        webhook_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new alert.
        
        Args:
            name: Name for the alert
            query: Search query string
            rate: Alert frequency (dly, wly, mly)
            alert_type: Type of alert (search, docket)
            webhook_url: Webhook URL for notifications
            **kwargs: Additional parameters
        
        Returns:
            Created alert data
        """
        data = {
            'name': name,
            'query': query,
            'rate': rate
        }
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
        Update an existing alert.
        
        Args:
            alert_id: Alert ID
            **kwargs: Fields to update
        
        Returns:
            Updated alert data
        """
        return self.client.post(f"{self.endpoint}{alert_id}/", data=kwargs)
    
    def delete(self, alert_id: int) -> bool:
        """
        Delete an alert.
        
        Args:
            alert_id: Alert ID
        
        Returns:
            True if successful
        """
        self.client._make_request('DELETE', f"{self.endpoint}{alert_id}/")
        return True
    
    def paginate(
        self,
        name: Optional[str] = None,
        alert_type: Optional[str] = None,
        **kwargs
    ):
        """
        Get paginated alerts.
        
        Args:
            name: Filter by alert name
            alert_type: Filter by alert type (search, docket)
            **kwargs: Additional query parameters
        
        Returns:
            PageIterator for alerts
        """
        params = {}
        if name is not None:
            params['name'] = name
        if alert_type is not None:
            params['alert_type'] = alert_type
        
        params.update(kwargs)
        return self.client.paginate(self.endpoint, params=params)
