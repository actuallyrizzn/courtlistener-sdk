"""
Integration tests for Financial Disclosures and related endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestFinancialDisclosuresIntegration:
    """Integration tests for financial disclosure endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_financial_disclosures_workflow(self):
        """Test complete financial disclosures workflow."""
        # Mock financial disclosures list
        mock_disclosures = {
            "count": 1,
            "results": [{
                "id": 1,
                "judge": "https://api.courtlistener.com/api/rest/v4/judges/123/",
                "year": 2023
            }]
        }
        self.client.get.return_value = mock_disclosures
        
        # Test getting financial disclosures
        disclosures = self.client.financial_disclosures.list(judge=123, year=2023)
        assert disclosures["count"] == 1
        assert len(disclosures["results"]) == 1
        
        # Mock investments for the disclosure
        mock_investments = {
            "count": 2,
            "results": [
                {"id": 1, "description": "Apple Stock", "value_min": 1000, "value_max": 5000},
                {"id": 2, "description": "Microsoft Stock", "value_min": 2000, "value_max": 6000}
            ]
        }
        self.client.get.return_value = mock_investments
        
        # Test getting investments
        investments = self.client.investments.list(financial_disclosure=1)
        assert investments["count"] == 2
        assert len(investments["results"]) == 2
        
        # Mock gifts for the disclosure
        mock_gifts = {
            "count": 1,
            "results": [{"id": 1, "description": "Conference attendance", "value": 2500}]
        }
        self.client.get.return_value = mock_gifts
        
        # Test getting gifts
        gifts = self.client.gifts.list(financial_disclosure=1)
        assert gifts["count"] == 1
        assert len(gifts["results"]) == 1
    
    def test_financial_disclosure_related_endpoints(self):
        """Test all financial disclosure related endpoints work together."""
        endpoints_to_test = [
            ('financial_disclosures', 'list', {'judge': 123}),
            ('investments', 'list', {'financial_disclosure': 1}),
            ('non_investment_incomes', 'list', {'financial_disclosure': 1}),
            ('agreements', 'list', {'financial_disclosure': 1}),
            ('gifts', 'list', {'financial_disclosure': 1}),
            ('reimbursements', 'list', {'financial_disclosure': 1}),
            ('debts', 'list', {'financial_disclosure': 1}),
            ('disclosure_positions', 'list', {'financial_disclosure': 1}),
            ('spouse_incomes', 'list', {'financial_disclosure': 1})
        ]
        
        mock_response = {"count": 0, "results": []}
        self.client.get.return_value = mock_response
        
        for endpoint_name, method_name, params in endpoints_to_test:
            endpoint = getattr(self.client, endpoint_name)
            method = getattr(endpoint, method_name)
            
            # Test that the method exists and can be called
            result = method(**params)
            assert result == mock_response
    
    def test_pagination_works_across_financial_endpoints(self):
        """Test that pagination works across all financial endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        financial_endpoints = [
            'financial_disclosures',
            'investments', 
            'non_investment_incomes',
            'agreements',
            'gifts',
            'reimbursements',
            'debts',
            'disclosure_positions',
            'spouse_incomes'
        ]
        
        for endpoint_name in financial_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.paginate()
            assert result == mock_iterator
    
    def test_get_methods_work_for_financial_endpoints(self):
        """Test that get methods work for all financial endpoints."""
        mock_response = {"id": 1, "description": "Test item"}
        self.client.get.return_value = mock_response
        
        financial_endpoints = [
            'financial_disclosures',
            'investments',
            'non_investment_incomes', 
            'agreements',
            'gifts',
            'reimbursements',
            'debts',
            'disclosure_positions',
            'spouse_incomes'
        ]
        
        for endpoint_name in financial_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.get(1)
            assert result == mock_response
