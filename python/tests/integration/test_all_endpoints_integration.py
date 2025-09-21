"""
Integration tests for all API endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestAllEndpointsIntegration:
    """Integration tests for all API endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_all_endpoints_are_available(self):
        """Test that all documented endpoints are available on the client."""
        # Core endpoints
        assert hasattr(self.client, 'search')
        assert hasattr(self.client, 'dockets')
        assert hasattr(self.client, 'opinions')
        assert hasattr(self.client, 'judges')
        assert hasattr(self.client, 'courts')
        assert hasattr(self.client, 'clusters')
        assert hasattr(self.client, 'positions')
        assert hasattr(self.client, 'audio')
        assert hasattr(self.client, 'financial')
        
        # Previously disabled endpoints - now enabled
        assert hasattr(self.client, 'docket_entries')
        assert hasattr(self.client, 'attorneys')
        assert hasattr(self.client, 'parties')
        assert hasattr(self.client, 'documents')
        assert hasattr(self.client, 'citations')
        
        # New endpoints
        assert hasattr(self.client, 'recap_documents')
        assert hasattr(self.client, 'financial_disclosures')
        assert hasattr(self.client, 'investments')
        assert hasattr(self.client, 'non_investment_incomes')
        assert hasattr(self.client, 'agreements')
        assert hasattr(self.client, 'gifts')
        assert hasattr(self.client, 'reimbursements')
        assert hasattr(self.client, 'debts')
        assert hasattr(self.client, 'disclosure_positions')
        assert hasattr(self.client, 'spouse_incomes')
        assert hasattr(self.client, 'opinions_cited')
        assert hasattr(self.client, 'alerts')
        assert hasattr(self.client, 'docket_alerts')
        assert hasattr(self.client, 'people')
        assert hasattr(self.client, 'schools')
        assert hasattr(self.client, 'educations')
        assert hasattr(self.client, 'sources')
        assert hasattr(self.client, 'retention_events')
        assert hasattr(self.client, 'aba_ratings')
        assert hasattr(self.client, 'political_affiliations')
        assert hasattr(self.client, 'tag')
        assert hasattr(self.client, 'recap_fetch')
        assert hasattr(self.client, 'recap_query')
        assert hasattr(self.client, 'originating_court_information')
        assert hasattr(self.client, 'fjc_integrated_database')
    
    def test_endpoints_have_list_method(self):
        """Test that all endpoints have a list method."""
        endpoints = [
            'search', 'dockets', 'opinions', 'judges', 'courts', 'clusters',
            'positions', 'audio', 'financial', 'docket_entries', 'attorneys',
            'parties', 'documents', 'citations', 'recap_documents',
            'financial_disclosures', 'investments', 'non_investment_incomes',
            'agreements', 'gifts', 'reimbursements', 'debts',
            'disclosure_positions', 'spouse_incomes', 'opinions_cited',
            'alerts', 'docket_alerts', 'people', 'schools', 'educations',
            'sources', 'retention_events', 'aba_ratings', 'political_affiliations',
            'tag', 'recap_fetch', 'recap_query', 'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in endpoints:
            endpoint = getattr(self.client, endpoint_name)
            assert hasattr(endpoint, 'list'), f"{endpoint_name} missing list method"
    
    def test_endpoints_have_get_method(self):
        """Test that all endpoints have a get method."""
        endpoints = [
            'search', 'dockets', 'opinions', 'judges', 'courts', 'clusters',
            'positions', 'audio', 'financial', 'docket_entries', 'attorneys',
            'parties', 'documents', 'citations', 'recap_documents',
            'financial_disclosures', 'investments', 'non_investment_incomes',
            'agreements', 'gifts', 'reimbursements', 'debts',
            'disclosure_positions', 'spouse_incomes', 'opinions_cited',
            'alerts', 'docket_alerts', 'people', 'schools', 'educations',
            'sources', 'retention_events', 'aba_ratings', 'political_affiliations',
            'tag', 'recap_fetch', 'recap_query', 'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in endpoints:
            endpoint = getattr(self.client, endpoint_name)
            assert hasattr(endpoint, 'get'), f"{endpoint_name} missing get method"
    
    def test_endpoints_have_paginate_method(self):
        """Test that all endpoints have a paginate method."""
        endpoints = [
            'search', 'dockets', 'opinions', 'judges', 'courts', 'clusters',
            'positions', 'audio', 'financial', 'docket_entries', 'attorneys',
            'parties', 'documents', 'citations', 'recap_documents',
            'financial_disclosures', 'investments', 'non_investment_incomes',
            'agreements', 'gifts', 'reimbursements', 'debts',
            'disclosure_positions', 'spouse_incomes', 'opinions_cited',
            'alerts', 'docket_alerts', 'people', 'schools', 'educations',
            'sources', 'retention_events', 'aba_ratings', 'political_affiliations',
            'tag', 'recap_fetch', 'recap_query', 'originating_court_information',
            'fjc_integrated_database'
        ]
        
        for endpoint_name in endpoints:
            endpoint = getattr(self.client, endpoint_name)
            assert hasattr(endpoint, 'paginate'), f"{endpoint_name} missing paginate method"
    
    def test_alerts_have_create_update_delete_methods(self):
        """Test that alerts endpoint has CRUD methods."""
        assert hasattr(self.client.alerts, 'create')
        assert hasattr(self.client.alerts, 'update')
        assert hasattr(self.client.alerts, 'delete')
    
    def test_docket_alerts_have_create_update_delete_methods(self):
        """Test that docket_alerts endpoint has CRUD methods."""
        assert hasattr(self.client.docket_alerts, 'create')
        assert hasattr(self.client.docket_alerts, 'update')
        assert hasattr(self.client.docket_alerts, 'delete')
    
    def test_no_disabled_endpoints(self):
        """Test that there are no disabled endpoints."""
        assert len(self.client._disabled_endpoints) == 0
