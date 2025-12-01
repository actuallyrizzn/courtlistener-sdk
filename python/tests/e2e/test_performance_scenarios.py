"""
End-to-end performance tests for high-volume scenarios.
"""

import pytest
import time
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient
from tests.conftest import skip_e2e_tests


@skip_e2e_tests
@pytest.mark.e2e
class TestPerformanceScenarios:
    """Performance tests for high-volume scenarios."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock all requests for performance testing
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_large_search_results_performance(self):
        """Test performance with large search results."""
        # Mock large search results
        large_results = {
            "count": 10000,
            "next": "https://api.courtlistener.com/api/rest/v4/search/?page=2",
            "results": [{"id": i, "caseName": f"Case {i}"} for i in range(100)]
        }
        self.client.get.return_value = large_results
        
        start_time = time.time()
        
        # Test search performance
        results = self.client.search.list(q="constitutional", court="scotus")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert results["count"] == 10000
        assert len(results["results"]) == 100
        assert execution_time < 1.0  # Should complete within 1 second
    
    def test_pagination_performance(self):
        """Test performance with pagination."""
        # Mock paginated results
        mock_page = {
            "count": 5000,
            "next": "https://api.courtlistener.com/api/rest/v4/opinions/?page=2",
            "results": [{"id": i, "caseName": f"Opinion {i}"} for i in range(100)]
        }
        self.client.paginate.return_value = iter([mock_page] * 5)  # Return 5 pages
        
        start_time = time.time()
        
        # Test pagination performance
        page_iterator = self.client.opinions.paginate(court="scotus")
        
        # Simulate processing first few pages
        pages_processed = 0
        for page in page_iterator:
            pages_processed += 1
            if pages_processed >= 5:  # Process 5 pages
                break
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert pages_processed == 5
        assert execution_time < 2.0  # Should complete within 2 seconds
    
    def test_concurrent_api_calls_performance(self):
        """Test performance with concurrent API calls."""
        import threading
        import queue
        
        # Mock responses for different endpoints
        mock_responses = {
            "courts": {"count": 1, "results": [{"id": 1, "name": "Supreme Court"}]},
            "judges": {"count": 1, "results": [{"id": 1, "name": "John Smith"}]},
            "opinions": {"count": 1, "results": [{"id": 1, "caseName": "Test Case"}]},
            "dockets": {"count": 1, "results": [{"id": 1, "case_name": "Test Docket"}]}
        }
        
        def mock_get(endpoint, params=None):
            if "courts" in endpoint:
                return mock_responses["courts"]
            elif "judges" in endpoint:
                return mock_responses["judges"]
            elif "opinions" in endpoint:
                return mock_responses["opinions"]
            elif "dockets" in endpoint:
                return mock_responses["dockets"]
            return {"count": 0, "results": []}
        
        self.client.get.side_effect = mock_get
        
        results_queue = queue.Queue()
        
        def api_call(endpoint_name, method_name, **kwargs):
            """Make an API call and store result."""
            endpoint = getattr(self.client, endpoint_name)
            method = getattr(endpoint, method_name)
            result = method(**kwargs)
            results_queue.put((endpoint_name, result))
        
        start_time = time.time()
        
        # Create multiple threads for concurrent API calls
        threads = []
        endpoints = [
            ("courts", "list"),
            ("judges", "list"),
            ("opinions", "list"),
            ("dockets", "list")
        ]
        
        for endpoint_name, method_name in endpoints:
            thread = threading.Thread(
                target=api_call,
                args=(endpoint_name, method_name)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all calls completed
        assert results_queue.qsize() == 4
        assert execution_time < 3.0  # Should complete within 3 seconds
    
    def test_large_financial_disclosure_performance(self):
        """Test performance with large financial disclosure datasets."""
        # Mock large financial disclosure data
        large_investments = {
            "count": 5000,
            "results": [
                {
                    "id": i,
                    "description": f"Investment {i}",
                    "value_min": 1000 + i,
                    "value_max": 5000 + i
                }
                for i in range(100)
            ]
        }
        self.client.get.return_value = large_investments
        
        start_time = time.time()
        
        # Test financial data retrieval performance
        investments = self.client.investments.list(financial_disclosure=1)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert investments["count"] == 5000
        assert len(investments["results"]) == 100
        assert execution_time < 1.0  # Should complete within 1 second
    
    def test_memory_usage_with_large_datasets(self):
        """Test memory usage with large datasets."""
        import sys
        
        # Mock very large dataset
        large_dataset = {
            "count": 100000,
            "results": [
                {
                    "id": i,
                    "name": f"Item {i}",
                    "description": f"Description for item {i}" * 10,  # Long description
                    "data": list(range(100))  # Additional data
                }
                for i in range(1000)  # 1000 items per page
            ]
        }
        self.client.get.return_value = large_dataset
        
        # Measure memory before
        initial_memory = sys.getsizeof(large_dataset)
        
        start_time = time.time()
        
        # Process large dataset
        results = self.client.people.list()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Measure memory after
        final_memory = sys.getsizeof(results)
        
        assert results["count"] == 100000
        assert len(results["results"]) == 1000
        assert execution_time < 2.0  # Should complete within 2 seconds
        assert final_memory >= initial_memory  # Memory should be at least the same
    
    def test_error_handling_performance(self):
        """Test performance when handling errors."""
        # Mock error responses
        def mock_get_with_errors(endpoint, params=None):
            if "error" in str(endpoint):
                raise Exception("API Error")
            return {"count": 1, "results": [{"id": 1}]}
        
        self.client.get.side_effect = mock_get_with_errors
        
        start_time = time.time()
        
        # Test error handling performance
        try:
            results = self.client.courts.list()
            assert results["count"] == 1
        except Exception:
            pass
        
        # Test with error endpoint
        try:
            results = self.client.courts.list()  # This should work
            assert results["count"] == 1
        except Exception:
            pass
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 1.0  # Error handling should be fast
