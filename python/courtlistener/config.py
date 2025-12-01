"""
Configuration management for the CourtListener SDK.
"""

import os
from typing import Optional
from .exceptions import ValidationError

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Configuration class for CourtListener SDK."""
    
    # Default settings
    DEFAULT_BASE_URL = "https://www.courtlistener.com/api/rest/v4/"
    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1
    DEFAULT_RATE_LIMIT_DELAY = 1
    DEFAULT_MAX_BACKOFF_DELAY = 60  # Maximum delay cap for exponential backoff
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        retry_delay: Optional[float] = None,
        rate_limit_delay: Optional[float] = None,
        max_backoff_delay: Optional[float] = None,
    ):
        """
        Initialize configuration.
        
        Args:
            api_token: CourtListener API token
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
            rate_limit_delay: Delay when rate limited in seconds
        """
        self.api_token = api_token or self._get_api_token_from_env()
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.max_retries = max_retries or self.DEFAULT_MAX_RETRIES
        self.retry_delay = retry_delay or self.DEFAULT_RETRY_DELAY
        self.rate_limit_delay = rate_limit_delay or self.DEFAULT_RATE_LIMIT_DELAY
        self.max_backoff_delay = max_backoff_delay or self.DEFAULT_MAX_BACKOFF_DELAY
        
        self._validate_config()
    
    def _get_api_token_from_env(self) -> Optional[str]:
        """Get API token from environment variables."""
        return os.getenv("COURTLISTENER_API_TOKEN")
    
    def _validate_config(self):
        """Validate configuration settings."""
        if not self.api_token:
            raise ValidationError("API token is required. Set COURTLISTENER_API_TOKEN environment variable or pass api_token parameter.")
        
        if self.timeout <= 0:
            raise ValidationError("Timeout must be greater than 0")
        
        if self.max_retries < 0:
            raise ValidationError("Max retries must be non-negative")
        
        if self.retry_delay < 0:
            raise ValidationError("Retry delay must be non-negative")
        
        if self.rate_limit_delay < 0:
            raise ValidationError("Rate limit delay must be non-negative")
    
    def get_headers(self) -> dict:
        """Get default headers for API requests."""
        return {
            "Authorization": f"Token {self.api_token}",
            "Content-Type": "application/json",
            "User-Agent": f"CourtListener-SDK/{self._get_version()}",
        }
    
    def _get_version(self) -> str:
        """Get SDK version."""
        try:
            from . import __version__
            return __version__
        except ImportError:
            return "0.1.0"
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"Config(base_url='{self.base_url}', timeout={self.timeout}, max_retries={self.max_retries})" 