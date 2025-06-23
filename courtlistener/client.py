"""
Main client class for the CourtListener SDK.
"""

import time
import requests
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin, urlencode

from .config import Config
from .exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError,
    ConnectionError,
    TimeoutError,
)
from .utils.pagination import PageIterator


class CourtListenerClient:
    """Main client for interacting with the CourtListener API."""
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        rate_limit_delay: Optional[float] = None,
    ):
        """
        Initialize CourtListener client.
        
        Args:
            api_token: CourtListener API token
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
            rate_limit_delay: Delay when rate limited in seconds
        """
        self.config = Config(
            api_token=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            rate_limit_delay=rate_limit_delay,
        )
        
        self.session = requests.Session()
        self.session.headers.update(self.config.get_headers())
        
        # Initialize API modules
        self._init_api_modules()
    
    def _init_api_modules(self):
        """Initialize API endpoint modules."""
        # Import API modules here to avoid circular imports
        from .api.search import SearchAPI
        from .api.dockets import DocketsAPI
        from .api.opinions import OpinionsAPI
        from .api.judges import JudgesAPI
        from .api.courts import CourtsAPI
        from .api.parties import PartiesAPI
        from .api.attorneys import AttorneysAPI
        from .api.documents import DocumentsAPI
        from .api.audio import AudioAPI
        from .api.financial import FinancialAPI
        from .api.citations import CitationsAPI
        
        # Initialize API modules
        self.search = SearchAPI(self)
        self.dockets = DocketsAPI(self)
        self.opinions = OpinionsAPI(self)
        self.judges = JudgesAPI(self)
        self.courts = CourtsAPI(self)
        self.parties = PartiesAPI(self)
        self.attorneys = AttorneysAPI(self)
        self.documents = DocumentsAPI(self)
        self.audio = AudioAPI(self)
        self.financial = FinancialAPI(self)
        self.citations = CitationsAPI(self)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            json_data: JSON data for POST requests
        
        Returns:
            API response data
        
        Raises:
            Various CourtListenerError subclasses for different error conditions
        """
        url = urljoin(self.config.base_url, endpoint)
        
        # Prepare request parameters
        request_kwargs = {
            'timeout': self.config.timeout,
        }
        
        if params:
            request_kwargs['params'] = params
        
        if data:
            request_kwargs['data'] = data
        
        if json_data:
            request_kwargs['json'] = json_data
        
        # Make request with retry logic
        for attempt in range(self.config.max_retries + 1):
            try:
                response = self.session.request(method, url, **request_kwargs)
                return self._handle_response(response)
            
            except requests.exceptions.Timeout:
                if attempt == self.config.max_retries:
                    raise TimeoutError("Request timed out")
                time.sleep(self.config.retry_delay)
            
            except requests.exceptions.ConnectionError:
                if attempt == self.config.max_retries:
                    raise ConnectionError("Failed to connect to API")
                time.sleep(self.config.retry_delay)
            
            except requests.exceptions.RequestException as e:
                if attempt == self.config.max_retries:
                    raise CourtListenerError(f"Request failed: {str(e)}")
                time.sleep(self.config.retry_delay)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and raise appropriate exceptions.
        
        Args:
            response: HTTP response object
        
        Returns:
            Response data as dictionary
        
        Raises:
            Various CourtListenerError subclasses based on response status
        """
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 401:
            raise AuthenticationError("Invalid API token")
        
        elif response.status_code == 404:
            raise NotFoundError("Resource not found")
        
        elif response.status_code == 429:
            # Rate limited - wait and retry
            time.sleep(self.config.rate_limit_delay)
            raise RateLimitError("Rate limit exceeded")
        
        elif response.status_code >= 500:
            raise APIError(f"Server error: {response.status_code}")
        
        else:
            # Try to get error message from response
            try:
                error_data = response.json()
                error_message = error_data.get('detail', f"HTTP {response.status_code}")
            except:
                error_message = f"HTTP {response.status_code}"
            
            raise APIError(error_message, response.status_code)
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to API endpoint."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make POST request to API endpoint."""
        return self._make_request('POST', endpoint, data=data, json_data=json_data)
    
    def paginate(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> PageIterator:
        """
        Get paginated results from an endpoint.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
        
        Returns:
            PageIterator for iterating through results
        """
        return PageIterator(self, endpoint, params)
    
    def test_connection(self) -> bool:
        """
        Test API connection by making a simple request.
        
        Returns:
            True if connection is successful
        
        Raises:
            CourtListenerError if connection fails
        """
        try:
            # Try to get courts list as a simple test
            self.get('courts/')
            return True
        except Exception as e:
            raise CourtListenerError(f"Connection test failed: {str(e)}")
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"CourtListenerClient(base_url='{self.config.base_url}')" 