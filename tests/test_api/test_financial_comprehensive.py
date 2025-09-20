"""
Comprehensive tests for Financial API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.financial import FinancialAPI, FinancialDisclosure, Investment, NonInvestmentIncome
from courtlistener.exceptions import ValidationError, CourtListenerError


class TestFinancialAPIComprehensive:
    """Comprehensive tests for FinancialAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = FinancialAPI(self.mock_client)
    
    def test_init(self):
        """Test FinancialAPI initialization."""
        assert self.api.client == self.mock_client
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "financial-disclosures/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == FinancialDisclosure
    
    def test_list_disclosures_basic(self):
        """Test basic list_disclosures functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_disclosures()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={})
    
    def test_list_disclosures_with_filters(self):
        """Test list_disclosures with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"judge": 1, "year": 2023}
        result = self.api.list_disclosures(filters=filters)
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params=filters)
    
    def test_get_disclosure_success(self):
        """Test get_disclosure with valid disclosure ID."""
        mock_response = {"id": 1, "judge": "John Smith", "year": 2023}
        self.mock_client.get.return_value = mock_response
        
        with patch('courtlistener.api.financial.validate_id') as mock_validate:
            result = self.api.get_disclosure(1)
            
            assert isinstance(result, FinancialDisclosure)
            mock_validate.assert_called_once_with(1)
            self.mock_client.get.assert_called_once_with("financial-disclosures/1/")
    
    def test_get_disclosure_invalid_id(self):
        """Test get_disclosure with invalid disclosure ID."""
        with patch('courtlistener.api.financial.validate_id') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid ID")
            
            with pytest.raises(ValidationError):
                self.api.get_disclosure(0)
            
            mock_validate.assert_called_once_with(0)
            self.mock_client.get.assert_not_called()
    
    def test_get_disclosure_not_found(self):
        """Test get_disclosure with non-existent disclosure ID."""
        with patch('courtlistener.api.financial.validate_id'):
            self.mock_client.get.side_effect = CourtListenerError("Disclosure not found")
            
            with pytest.raises(CourtListenerError):
                self.api.get_disclosure(999)
    
    def test_list_financial_basic(self):
        """Test basic list_financial functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_financial()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 1})
    
    def test_list_financial_with_page(self):
        """Test list_financial with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_financial(page=2)
        
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 2})
    
    def test_list_financial_with_filters(self):
        """Test list_financial with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"judge": 1, "year": 2023}
        self.api.list_financial(page=1, **filters)
        
        expected_params = {"page": 1, "judge": 1, "year": 2023}
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params=expected_params)
    
    def test_list_financial_no_filters(self):
        """Test list_financial with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_financial(page=1)
        
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 1})
    
    def test_search_financial_basic(self):
        """Test basic search_financial functionality."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_financial()
        
        assert result == mock_response
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 1})
    
    def test_search_financial_with_page(self):
        """Test search_financial with specific page."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_financial(page=2)
        
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 2})
    
    def test_search_financial_with_filters(self):
        """Test search_financial with filters."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        filters = {"judge": 1, "year": 2023}
        self.api.search_financial(page=1, **filters)
        
        expected_params = {"page": 1, "judge": 1, "year": 2023}
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params=expected_params)
    
    def test_search_financial_no_filters(self):
        """Test search_financial with no filters parameter."""
        mock_response = {"results": [], "count": 0}
        self.mock_client.get.return_value = mock_response
        
        self.api.search_financial(page=1)
        
        self.mock_client.get.assert_called_once_with("financial-disclosures/", params={"page": 1})
    
    def test_list_financial_disclosures_basic(self):
        """Test basic list_financial_disclosures functionality."""
        mock_response = {
            "results": [
                {"id": 1, "judge": "John Smith"},
                {"id": 2, "judge": "Jane Doe"}
            ]
        }
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_financial_disclosures()
        
        assert len(result) == 2
        assert all(isinstance(d, FinancialDisclosure) for d in result)
        self.mock_client._make_request.assert_called_once_with("GET", "/financial-disclosures/", params={"page": 1})
    
    def test_list_financial_disclosures_with_page(self):
        """Test list_financial_disclosures with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.list_financial_disclosures(page=2)
        
        self.mock_client._make_request.assert_called_once_with("GET", "/financial-disclosures/", params={"page": 2})
    
    def test_list_financial_disclosures_with_query(self):
        """Test list_financial_disclosures with search query."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        self.api.list_financial_disclosures(q="smith")
        
        self.mock_client._make_request.assert_called_once_with("GET", "/financial-disclosures/", params={"page": 1, "q": "smith"})
    
    def test_list_financial_disclosures_with_filters(self):
        """Test list_financial_disclosures with filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"judge": 1, "year": 2023}
        self.api.list_financial_disclosures(page=1, **filters)
        
        expected_params = {"page": 1, "judge": 1, "year": 2023}
        self.mock_client._make_request.assert_called_once_with("GET", "/financial-disclosures/", params=expected_params)
    
    def test_list_financial_disclosures_with_query_and_filters(self):
        """Test list_financial_disclosures with both query and filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        filters = {"judge": 1}
        self.api.list_financial_disclosures(q="smith", page=2, **filters)
        
        expected_params = {"page": 2, "q": "smith", "judge": 1}
        self.mock_client._make_request.assert_called_once_with("GET", "/financial-disclosures/", params=expected_params)
    
    def test_list_financial_disclosures_empty_results(self):
        """Test list_financial_disclosures with empty results."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_financial_disclosures()
        
        assert result == []
    
    def test_list_financial_disclosures_no_results_key(self):
        """Test list_financial_disclosures when response has no results key."""
        mock_response = {}
        self.mock_client._make_request.return_value = mock_response
        
        result = self.api.list_financial_disclosures()
        
        assert result == []
    
    def test_search_financial_disclosures_basic(self):
        """Test search_financial_disclosures without filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_financial_disclosures') as mock_list:
            mock_list.return_value = []
            
            result = self.api.search_financial_disclosures("smith")
            
            mock_list.assert_called_once_with(page=1, q="smith")
            assert result == []
    
    def test_search_financial_disclosures_with_page(self):
        """Test search_financial_disclosures with specific page."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_financial_disclosures') as mock_list:
            mock_list.return_value = []
            
            self.api.search_financial_disclosures("smith", page=2)
            
            mock_list.assert_called_once_with(page=2, q="smith")
    
    def test_search_financial_disclosures_with_filters(self):
        """Test search_financial_disclosures with filters."""
        mock_response = {"results": []}
        self.mock_client._make_request.return_value = mock_response
        
        with patch.object(self.api, 'list_financial_disclosures') as mock_list:
            mock_list.return_value = []
            
            filters = {"judge": 1}
            self.api.search_financial_disclosures("smith", page=1, **filters)
            
            mock_list.assert_called_once_with(page=1, q="smith", judge=1)
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_financial()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client._make_request.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.list_financial_disclosures()
