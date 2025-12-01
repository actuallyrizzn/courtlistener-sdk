"""
Live API tests for performance and load testing.
These tests require a valid API token and will make real API calls.
"""

import pytest
import os
import time
import threading
from courtlistener import CourtListenerClient
from courtlistener.exceptions import CourtListenerError
from tests.conftest import skip_live_tests


@skip_live_tests
@pytest.mark.live
class TestLiveAPIPerformance:
    """Live API tests for performance."""
    
    @classmethod
    def setup_class(cls):
        """Set up test class with API token."""
        api_token = os.getenv('COURTLISTENER_API_TOKEN')
        if not api_token:
            pytest.skip("COURTLISTENER_API_TOKEN environment variable not set")
        
        cls.client = CourtListenerClient(api_token=api_token)
    
    def test_response_times(self):
        """Test response times for various endpoints."""
        endpoints_to_test = [
            ('courts', 'list', {}),
            ('opinions', 'list', {'page_size': 10}),
            ('dockets', 'list', {'page_size': 10}),
            ('judges', 'list', {'page_size': 10}),
            ('search', 'list', {'q': 'constitutional', 'page_size': 10})
        ]
        
        for endpoint_name, method_name, params in endpoints_to_test:
            endpoint = getattr(self.client, endpoint_name)
            method = getattr(endpoint, method_name)
            
            start_time = time.time()
            try:
                result = method(**params)
                end_time = time.time()
                response_time = end_time - start_time
                
                assert 'count' in result
                assert response_time < 10.0  # Should respond within 10 seconds
                print(f"{endpoint_name}.{method_name} response time: {response_time:.2f}s")
                
            except CourtListenerError as e:
                print(f"{endpoint_name}.{method_name} failed: {e}")
                # Some endpoints may not be accessible, which is acceptable
    
    def test_concurrent_requests(self):
        """Test performance with concurrent requests."""
        def make_request():
            """Make a single API request."""
            start_time = time.time()
            try:
                result = self.client.courts.list(page_size=5)
                end_time = time.time()
                return end_time - start_time, result
            except CourtListenerError as e:
                return None, e
        
        # Test with 5 concurrent requests
        threads = []
        results = []
        
        start_time = time.time()
        
        for _ in range(5):
            thread = threading.Thread(
                target=lambda: results.append(make_request())
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify results
        successful_requests = [r for r in results if r[0] is not None]
        assert len(successful_requests) >= 1  # At least one should succeed
        
        # Check that concurrent requests completed reasonably quickly
        assert total_time < 15.0  # All requests should complete within 15 seconds
        
        print(f"Concurrent requests completed in {total_time:.2f}s")
    
    def test_large_dataset_handling(self):
        """Test handling of large datasets."""
        # Test with larger page sizes
        start_time = time.time()
        
        try:
            result = self.client.opinions.list(page_size=100)
            end_time = time.time()
            response_time = end_time - start_time
            
            assert 'count' in result
            assert 'results' in result
            assert len(result['results']) <= 100
            assert response_time < 15.0  # Should handle large pages within 15 seconds
            
            print(f"Large dataset (100 items) response time: {response_time:.2f}s")
            
        except CourtListenerError as e:
            print(f"Large dataset test failed: {e}")
            # Some APIs may not support large page sizes
    
    def test_pagination_performance(self):
        """Test pagination performance."""
        start_time = time.time()
        
        try:
            # Test pagination with small page size
            pages = []
            page_count = 0
            
            for page in self.client.opinions.paginate(page_size=5):
                pages.append(page)
                page_count += 1
                if page_count >= 3:  # Limit to 3 pages for performance testing
                    break
            
            end_time = time.time()
            total_time = end_time - start_time
            
            assert len(pages) >= 1
            assert total_time < 20.0  # Should complete within 20 seconds
            
            print(f"Pagination (3 pages) completed in {total_time:.2f}s")
            
        except CourtListenerError as e:
            print(f"Pagination test failed: {e}")
    
    def test_search_performance(self):
        """Test search performance with various queries."""
        search_queries = [
            "constitutional law",
            "Miranda rights",
            "first amendment",
            "due process",
            "equal protection"
        ]
        
        for query in search_queries:
            start_time = time.time()
            
            try:
                result = self.client.search.list(q=query, page_size=10)
                end_time = time.time()
                response_time = end_time - start_time
                
                assert 'count' in result
                assert 'results' in result
                assert response_time < 10.0  # Each search should complete within 10 seconds
                
                print(f"Search '{query}' response time: {response_time:.2f}s")
                
            except CourtListenerError as e:
                print(f"Search '{query}' failed: {e}")
    
    def test_filtering_performance(self):
        """Test filtering performance."""
        filters_to_test = [
            {'court': 'scotus'},
            {'date_filed__gte': '2020-01-01'},
            {'court': 'scotus', 'date_filed__gte': '2020-01-01'}
        ]
        
        for filters in filters_to_test:
            start_time = time.time()
            
            try:
                result = self.client.opinions.list(page_size=10, **filters)
                end_time = time.time()
                response_time = end_time - start_time
                
                assert 'count' in result
                assert 'results' in result
                assert response_time < 10.0  # Filtering should complete within 10 seconds
                
                filter_str = ', '.join(f"{k}={v}" for k, v in filters.items())
                print(f"Filter {filter_str} response time: {response_time:.2f}s")
                
            except CourtListenerError as e:
                print(f"Filter {filters} failed: {e}")
    
    def test_memory_usage(self):
        """Test memory usage with large responses."""
        import sys
        
        start_time = time.time()
        
        try:
            # Get a large response
            result = self.client.opinions.list(page_size=50)
            end_time = time.time()
            response_time = end_time - start_time
            
            # Check memory usage
            memory_usage = sys.getsizeof(result)
            
            assert 'count' in result
            assert 'results' in result
            assert response_time < 15.0
            assert memory_usage < 1024 * 1024  # Should use less than 1MB
            
            print(f"Memory usage: {memory_usage} bytes")
            print(f"Large response time: {response_time:.2f}s")
            
        except CourtListenerError as e:
            print(f"Memory usage test failed: {e}")
    
    def test_error_recovery_performance(self):
        """Test error recovery performance."""
        # Test with invalid parameters that might cause errors
        invalid_requests = [
            {'court': 'invalid_court'},
            {'date_filed__gte': 'invalid_date'},
            {'page_size': -1}
        ]
        
        for invalid_params in invalid_requests:
            start_time = time.time()
            
            try:
                result = self.client.opinions.list(**invalid_params)
                end_time = time.time()
                response_time = end_time - start_time
                
                # If it doesn't error, it should respond quickly
                assert response_time < 5.0
                print(f"Invalid params {invalid_params} handled in {response_time:.2f}s")
                
            except CourtListenerError as e:
                end_time = time.time()
                response_time = end_time - start_time
                
                # Error handling should also be fast
                assert response_time < 5.0
                print(f"Invalid params {invalid_params} errored in {response_time:.2f}s")
    
    def test_rate_limiting_behavior(self):
        """Test rate limiting behavior."""
        # Make multiple requests quickly to test rate limiting
        request_times = []
        
        for i in range(10):
            start_time = time.time()
            
            try:
                result = self.client.courts.list(page_size=1)
                end_time = time.time()
                request_time = end_time - start_time
                request_times.append(request_time)
                
                assert 'count' in result
                
            except CourtListenerError as e:
                end_time = time.time()
                request_time = end_time - start_time
                request_times.append(request_time)
                
                # If we hit rate limits, that's expected behavior
                if "rate limit" in str(e).lower():
                    print(f"Rate limit hit at request {i+1}")
                    break
        
        # Check that requests are completing reasonably
        if request_times:
            avg_time = sum(request_times) / len(request_times)
            assert avg_time < 5.0  # Average request time should be reasonable
            
            print(f"Average request time: {avg_time:.2f}s")
            print(f"Total requests made: {len(request_times)}")
    
    def test_endpoint_availability(self):
        """Test availability of all endpoints."""
        endpoints_to_test = [
            'courts', 'opinions', 'dockets', 'judges', 'clusters',
            'positions', 'audio', 'financial', 'search'
        ]
        
        available_endpoints = []
        unavailable_endpoints = []
        
        for endpoint_name in endpoints_to_test:
            start_time = time.time()
            
            try:
                endpoint = getattr(self.client, endpoint_name)
                result = endpoint.list(page_size=1)
                end_time = time.time()
                response_time = end_time - start_time
                
                assert 'count' in result
                available_endpoints.append((endpoint_name, response_time))
                
            except CourtListenerError as e:
                end_time = time.time()
                response_time = end_time - start_time
                unavailable_endpoints.append((endpoint_name, str(e), response_time))
        
        # Report results
        print(f"Available endpoints: {len(available_endpoints)}")
        for endpoint, time_taken in available_endpoints:
            print(f"  {endpoint}: {time_taken:.2f}s")
        
        print(f"Unavailable endpoints: {len(unavailable_endpoints)}")
        for endpoint, error, time_taken in unavailable_endpoints:
            print(f"  {endpoint}: {error} ({time_taken:.2f}s)")
        
        # At least some endpoints should be available
        assert len(available_endpoints) >= 3
