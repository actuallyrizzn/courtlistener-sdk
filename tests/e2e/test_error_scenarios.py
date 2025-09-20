"""
End-to-end tests for error scenarios and edge cases.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    APIError,
    ConnectionError,
    TimeoutError
)


class TestErrorScenarios:
    """End-to-end tests for error scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_authentication_error_handling(self):
        """Test handling of authentication errors."""
        # Mock 401 response
        self.client.get.side_effect = AuthenticationError("Invalid API token")
        
        with pytest.raises(AuthenticationError):
            self.client.courts.list()
    
    def test_rate_limit_error_handling(self):
        """Test handling of rate limit errors."""
        # Mock 429 response
        self.client.get.side_effect = RateLimitError("Rate limit exceeded")
        
        with pytest.raises(RateLimitError):
            self.client.opinions.list()
    
    def test_not_found_error_handling(self):
        """Test handling of not found errors."""
        # Mock 404 response
        self.client.get.side_effect = NotFoundError("Resource not found")
        
        with pytest.raises(NotFoundError):
            self.client.opinions.get(999999)
    
    def test_api_error_handling(self):
        """Test handling of general API errors."""
        # Mock 500 response
        self.client.get.side_effect = APIError("Internal server error", 500)
        
        with pytest.raises(APIError):
            self.client.dockets.list()
    
    def test_connection_error_handling(self):
        """Test handling of connection errors."""
        # Mock connection error
        self.client.get.side_effect = ConnectionError("Failed to connect to API")
        
        with pytest.raises(ConnectionError):
            self.client.search.list(q="test")
    
    def test_timeout_error_handling(self):
        """Test handling of timeout errors."""
        # Mock timeout error
        self.client.get.side_effect = TimeoutError("Request timed out")
        
        with pytest.raises(TimeoutError):
            self.client.audio.list()
    
    def test_invalid_parameters_error_handling(self):
        """Test handling of invalid parameters."""
        # Mock 400 response
        self.client.post.side_effect = APIError("Invalid parameters", 400)
        
        with pytest.raises(APIError):
            self.client.alerts.create(
                name="",  # Invalid empty name
                query="test",
                rate="invalid_rate"  # Invalid rate
            )
    
    def test_malformed_response_handling(self):
        """Test handling of malformed responses."""
        # Mock malformed JSON response by raising ValueError in get
        self.client.get.side_effect = ValueError("Invalid JSON")
        
        with pytest.raises(ValueError):
            self.client.courts.list()
    
    def test_empty_response_handling(self):
        """Test handling of empty responses."""
        # Mock empty response
        self.client.get.return_value = {}
        
        # Should handle empty response gracefully
        result = self.client.courts.list()
        assert result == {}
    
    def test_partial_response_handling(self):
        """Test handling of partial responses."""
        # Mock partial response (missing expected fields)
        partial_response = {
            "count": 1,
            # Missing "results" field
        }
        
        self.client.get.return_value = partial_response
        
        # Should handle partial response gracefully
        result = self.client.opinions.list()
        assert result["count"] == 1
        assert "results" not in result
    
    def test_large_error_response_handling(self):
        """Test handling of large error responses."""
        # Mock large error response
        large_error = {
            "detail": "Error message " * 1000,  # Very long error message
            "errors": [{"field": f"field_{i}", "message": f"error_{i}"} for i in range(100)]
        }
        
        self.client.post.return_value = large_error
        
        # Should handle large error response
        result = self.client.alerts.create(name="test", query="test", rate="wly")
        assert "detail" in result
        assert len(result["detail"]) > 1000
    
    def test_concurrent_error_handling(self):
        """Test handling of errors in concurrent requests."""
        import threading
        import queue
        
        error_queue = queue.Queue()
        
        def api_call_with_error():
            """Make an API call that will error."""
            try:
                self.client.get.side_effect = APIError("Concurrent error", 500)
                self.client.courts.list()
            except APIError as e:
                error_queue.put(e)
        
        # Create multiple threads that will all error
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=api_call_with_error)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all errors were caught
        assert error_queue.qsize() == 5
        
        # Verify all errors are APIError instances
        while not error_queue.empty():
            error = error_queue.get()
            assert isinstance(error, APIError)
    
    def test_retry_mechanism_with_errors(self):
        """Test retry mechanism with intermittent errors."""
        # Mock API error that should be retried
        self.client.get.side_effect = APIError("Temporary error", 500)
        
        # Should raise the API error (retry logic is tested in integration tests)
        with pytest.raises(APIError, match="Temporary error"):
            self.client.courts.list()
    
    def test_error_recovery_scenarios(self):
        """Test various error recovery scenarios."""
        # Test recovery from authentication error
        self.client.get.side_effect = AuthenticationError("Invalid token")
        
        with pytest.raises(AuthenticationError):
            self.client.courts.list()
        
        # Test recovery from rate limit error
        self.client.get.side_effect = RateLimitError("Rate limit exceeded")
        
        with pytest.raises(RateLimitError):
            self.client.opinions.list()
        
        # Test recovery from connection error
        self.client.get.side_effect = ConnectionError("Connection failed")
        
        with pytest.raises(ConnectionError):
            self.client.search.list(q="test")
        
        # Test successful recovery
        self.client.get.side_effect = None
        self.client.get.return_value = {"count": 1, "results": [{"id": 1}]}
        
        result = self.client.courts.list()
        assert result["count"] == 1
