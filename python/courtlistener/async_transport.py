"""
Async HTTP Transport layer for the CourtListener SDK.

This module handles all async HTTP communication, retries, timeouts, and response processing.
"""

import asyncio
import httpx
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

from .exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError,
    AcceptedError,
    ConnectionError,
    TimeoutError,
)


class AsyncTransport:
    """Handles async HTTP transport for API requests."""
    
    def __init__(self, config):
        """
        Initialize async transport layer.
        
        Args:
            config: Configuration object with API settings
        """
        self.config = config
        self.client = None  # Will be initialized in __aenter__
        self.logger = logging.getLogger(__name__)
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.client = httpx.AsyncClient(
            headers=self.config.get_headers(),
            timeout=self.config.timeout,
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.client:
            await self.client.aclose()
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make async HTTP request to the API.
        
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
        # Ensure proper URL construction - urljoin can remove path components
        if endpoint.startswith('/'):
            url = self.config.base_url.rstrip('/') + endpoint
        else:
            url = urljoin(self.config.base_url, endpoint)
        
        # Prepare request parameters
        request_kwargs = {}
        
        if params:
            request_kwargs['params'] = params
        
        if data:
            request_kwargs['data'] = data
        
        if json_data:
            request_kwargs['json'] = json_data
        
        # Make request with retry logic
        for attempt in range(self.config.max_retries + 1):
            try:
                response = await self.client.request(method, url, **request_kwargs)
                return self._handle_response(response)
            
            except httpx.TimeoutException as exc:
                if attempt == self.config.max_retries:
                    detail = str(exc).strip()
                    message = "Request timed out"
                    if detail:
                        message = f"{message}: {detail}"
                    raise TimeoutError(message)
                await asyncio.sleep(self.config.retry_delay)
            
            except httpx.ConnectError as exc:
                if attempt == self.config.max_retries:
                    detail = str(exc).strip()
                    message = "Failed to connect to API"
                    if detail:
                        message = f"{message}: {detail}"
                    raise ConnectionError(message)
                await asyncio.sleep(self.config.retry_delay)
            
            except httpx.RequestError as e:
                if attempt == self.config.max_retries:
                    raise CourtListenerError(f"Request failed: {str(e)}")
                await asyncio.sleep(self.config.retry_delay)
            
            except APIError as e:
                if attempt == self.config.max_retries:
                    raise e
                await asyncio.sleep(self.config.retry_delay)
            
            except RateLimitError as e:
                if attempt == self.config.max_retries:
                    raise e
                # Use retry_after if available, otherwise use rate_limit_delay
                delay = getattr(e, 'retry_after', None) or self.config.rate_limit_delay
                await asyncio.sleep(delay)
            
            except AcceptedError as e:
                if attempt == self.config.max_retries:
                    raise e
                # Use retry_after if available, otherwise use retry_delay
                delay = getattr(e, 'retry_after', None) or self.config.retry_delay
                await asyncio.sleep(delay)
    
    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
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
            # Rate limited - extract Retry-After header if present
            retry_after = None
            if 'Retry-After' in response.headers:
                try:
                    retry_after = int(response.headers['Retry-After'])
                except (ValueError, TypeError):
                    pass
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        
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
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async GET request to API endpoint."""
        return await self._make_request('GET', endpoint, params=params)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async POST request to API endpoint."""
        return await self._make_request('POST', endpoint, data=data, json_data=json_data)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async PUT request to API endpoint."""
        return await self._make_request('PUT', endpoint, data=data, json_data=json_data)
    
    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make async PATCH request to API endpoint."""
        return await self._make_request('PATCH', endpoint, data=data, json_data=json_data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make async DELETE request to API endpoint."""
        return await self._make_request('DELETE', endpoint)
