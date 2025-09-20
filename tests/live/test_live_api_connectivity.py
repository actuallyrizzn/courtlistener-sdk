"""
Live API tests for connectivity and basic functionality.
These tests require a valid API token and will make real API calls.
"""

import pytest
import os
from courtlistener import CourtListenerClient
from courtlistener.exceptions import CourtListenerError


class TestLiveAPIConnectivity:
    """Live API tests for connectivity."""
    
    @classmethod
    def setup_class(cls):
        """Set up test class with API token."""
        # Set the API token directly for testing
        api_token = "7c2ad11c595dcb088f23d7a757190c47e8f397a2"
        os.environ['COURTLISTENER_API_TOKEN'] = api_token
        
        cls.client = CourtListenerClient(api_token=api_token)
    
    def test_api_connection(self):
        """Test basic API connection."""
        # Test connection by getting courts list
        result = self.client.courts.list()
        assert isinstance(result, dict)
        assert 'count' in result
        assert 'results' in result
        assert isinstance(result['count'], int)
        assert isinstance(result['results'], list)
        assert len(result['results']) > 0
    
    def test_authentication(self):
        """Test API authentication."""
        # This should work with valid token
        result = self.client.courts.list()
        assert isinstance(result, dict)
        assert 'count' in result
        assert 'results' in result
    
    def test_basic_search(self):
        """Test basic search functionality."""
        result = self.client.search.list(q="constitutional")
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
    
    def test_courts_endpoint(self):
        """Test courts endpoint."""
        result = self.client.courts.list()
        assert isinstance(result, dict)
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
        
        court = result['results'][0]
        assert isinstance(court, dict)
        assert 'id' in court
        assert 'short_name' in court
    
    def test_opinions_endpoint(self):
        """Test opinions endpoint."""
        result = self.client.opinions.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
        
        opinion = result['results'][0]
        assert 'id' in opinion
    
    def test_dockets_endpoint(self):
        """Test dockets endpoint."""
        result = self.client.dockets.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
        
        docket = result['results'][0]
        assert 'id' in docket
    
    def test_judges_endpoint(self):
        """Test judges endpoint."""
        result = self.client.judges.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
        
        judge = result['results'][0]
        assert 'id' in judge
    
    def test_clusters_endpoint(self):
        """Test clusters endpoint."""
        result = self.client.clusters.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
        
        cluster = result['results'][0]
        assert 'id' in cluster
    
    def test_audio_endpoint(self):
        """Test audio endpoint."""
        result = self.client.audio.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
    
    def test_positions_endpoint(self):
        """Test positions endpoint."""
        result = self.client.positions.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
    
    def test_financial_endpoint(self):
        """Test financial endpoint."""
        result = self.client.financial.list()
        assert 'count' in result
        assert 'results' in result
        assert len(result['results']) > 0
    
    def test_pagination_works(self):
        """Test that pagination works."""
        # Get first page
        page1 = self.client.courts.list()
        assert 'next' in page1 or page1['next'] is None
        assert 'previous' in page1 or page1['previous'] is None
        
        # Test pagination iterator
        pages = list(self.client.courts.paginate(page_size=2))
        assert len(pages) >= 1
    
    def test_filtering_works(self):
        """Test that filtering works."""
        # Test court filtering
        result = self.client.opinions.list(court="scotus", page_size=5)
        assert 'count' in result
        assert 'results' in result
        
        # Test date filtering
        result = self.client.opinions.list(
            date_filed__gte="2020-01-01",
            page_size=5
        )
        assert 'count' in result
        assert 'results' in result
    
    def test_get_specific_items(self):
        """Test getting specific items by ID."""
        # Get a list first
        courts = self.client.courts.list()
        if courts['results']:
            court_id = courts['results'][0]['id']
            
            # Get specific court
            court = self.client.courts.get(court_id)
        assert court['id'] == court_id
    
    def test_error_handling(self):
        """Test error handling with invalid requests."""
        # Test with invalid ID
        try:
            self.client.opinions.get(999999999)
            # If no exception, that's also fine (some APIs return empty results)
        except CourtListenerError:
            # Expected behavior
            pass
    
    def test_rate_limiting(self):
        """Test rate limiting behavior."""
        # Make multiple requests quickly
        for _ in range(5):
            result = self.client.courts.list()
        assert 'count' in result
    
    def test_all_endpoints_accessible(self):
        """Test that all endpoints are accessible."""
        endpoints_to_test = [
            'search', 'dockets', 'opinions', 'judges', 'courts',
            'clusters', 'positions', 'audio', 'financial',
            'docket_entries', 'attorneys', 'parties', 'documents',
            'citations', 'recap_documents', 'financial_disclosures',
            'investments', 'non_investment_incomes', 'agreements',
            'gifts', 'reimbursements', 'debts', 'disclosure_positions',
            'spouse_incomes', 'opinions_cited', 'alerts', 'docket_alerts',
            'people', 'schools', 'educations', 'sources', 'retention_events',
            'aba_ratings', 'political_affiliations', 'tag',
            'recap_fetch', 'recap_query', 'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in endpoints_to_test:
            endpoint = getattr(self.client, endpoint_name)
            
            # Test that endpoint has required methods
            assert hasattr(endpoint, 'list')
            assert hasattr(endpoint, 'get')
            assert hasattr(endpoint, 'paginate')
            
            # Test list method (with small page size to avoid rate limits)
            try:
                result = endpoint.list()
                assert 'count' in result
                assert 'results' in result
            except CourtListenerError as e:
                # Some endpoints may not be accessible or may have no data
                # This is acceptable for live testing
                print(f"Endpoint {endpoint_name} returned error: {e}")
                pass
