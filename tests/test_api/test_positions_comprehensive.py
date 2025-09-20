"""
Comprehensive tests for Positions API to achieve 100% coverage.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener.api.positions import PositionsAPI
from courtlistener.models.position import Position
from courtlistener.exceptions import NotFoundError, CourtListenerError


class TestPositionsAPIComprehensive:
    """Comprehensive tests for PositionsAPI to achieve 100% coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_client = Mock()
        self.api = PositionsAPI(self.mock_client)
    
    def test_init(self):
        """Test PositionsAPI initialization."""
        assert self.api.client == self.mock_client
        assert self.api.base_url == "/api/rest/v4/positions/"
    
    def test_get_endpoint(self):
        """Test _get_endpoint method."""
        assert self.api._get_endpoint() == "positions/"
    
    def test_get_model_class(self):
        """Test _get_model_class method."""
        assert self.api._get_model_class() == Position
    
    def test_list_positions_basic(self):
        """Test basic list_positions functionality."""
        mock_response = {
            "results": [
                {"id": 1, "position_type": "jud"},
                {"id": 2, "position_type": "mag"}
            ]
        }
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_positions()
        
        assert len(result) == 2
        assert all(isinstance(p, Position) for p in result)
        self.mock_client.get.assert_called_once_with("/positions/", params={"page": 1})
    
    def test_list_positions_with_page(self):
        """Test list_positions with specific page."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_positions(page=2)
        
        self.mock_client.get.assert_called_once_with("/positions/", params={"page": 2})
    
    def test_list_positions_with_query(self):
        """Test list_positions with search query."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.list_positions(q="test query")
        
        self.mock_client.get.assert_called_once_with("/positions/", params={"page": 1, "q": "test query"})
    
    def test_list_positions_with_filters(self):
        """Test list_positions with filters."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        filters = {"court": 1, "position_type": "jud"}
        self.api.list_positions(page=1, **filters)
        
        expected_params = {"page": 1, "court": 1, "position_type": "jud"}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_list_positions_empty_results(self):
        """Test list_positions with empty results."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_positions()
        
        assert result == []
    
    def test_list_positions_no_results_key(self):
        """Test list_positions when response has no results key."""
        mock_response = {}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.list_positions()
        
        assert result == []
    
    def test_search_positions(self):
        """Test search_positions method."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.search_positions("test query", page=2, court=1)
        
        assert len(result) == 1
        expected_params = {"page": 2, "q": "test query", "court": 1}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_position_success(self):
        """Test get_position with valid position ID."""
        mock_response = {"id": 1, "position_type": "jud"}
        self.mock_client.get.return_value = mock_response
        
        with patch.object(Position, 'from_dict') as mock_from_dict:
            mock_position = Mock(spec=Position)
            mock_from_dict.return_value = mock_position
            
            result = self.api.get_position(1)
            
            assert result == mock_position
            self.mock_client.get.assert_called_once_with("/api/rest/v4/positions/1/")
            mock_from_dict.assert_called_once_with(mock_response)
    
    def test_get_position_not_found(self):
        """Test get_position with non-existent position ID."""
        self.mock_client.get.side_effect = NotFoundError("Position not found")
        
        with pytest.raises(NotFoundError):
            self.api.get_position(999)
    
    def test_get_positions_by_judge_basic(self):
        """Test get_positions_by_judge without limit."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_judge(1)
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"judge": 1}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_judge_with_limit(self):
        """Test get_positions_by_judge with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_judge(1, limit=10)
        
        expected_params = {"page": 1, "filters": {"judge": 1}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_court_basic(self):
        """Test get_positions_by_court without limit."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_court(1)
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"court": 1}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_court_with_limit(self):
        """Test get_positions_by_court with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_court(1, limit=10)
        
        expected_params = {"page": 1, "filters": {"court": 1}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_active_positions_basic(self):
        """Test get_active_positions without court filter."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_active_positions()
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"date_termination__isnull": True}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_active_positions_with_court(self):
        """Test get_active_positions with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_active_positions(court_id=1)
        
        expected_params = {"page": 1, "filters": {"date_termination__isnull": True, "court": 1}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_active_positions_with_limit(self):
        """Test get_active_positions with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_active_positions(limit=10)
        
        expected_params = {"page": 1, "filters": {"date_termination__isnull": True}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_position_type_basic(self):
        """Test get_positions_by_position_type without court filter."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_position_type("jud")
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"position_type": "jud"}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_position_type_with_court(self):
        """Test get_positions_by_position_type with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_position_type("jud", court_id=1)
        
        expected_params = {"page": 1, "filters": {"position_type": "jud", "court": 1}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_position_type_with_limit(self):
        """Test get_positions_by_position_type with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_position_type("jud", limit=10)
        
        expected_params = {"page": 1, "filters": {"position_type": "jud"}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_date_range_basic(self):
        """Test get_positions_by_date_range without court filter."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_date_range("2023-01-01", "2023-12-31")
        
        assert len(result) == 1
        expected_params = {
            "page": 1,
            "filters": {
                "date_start__gte": "2023-01-01",
                "date_start__lte": "2023-12-31"
            },
            "limit": None
        }
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_date_range_with_court(self):
        """Test get_positions_by_date_range with court filter."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_date_range("2023-01-01", "2023-12-31", court_id=1)
        
        expected_params = {
            "page": 1,
            "filters": {
                "date_start__gte": "2023-01-01",
                "date_start__lte": "2023-12-31",
                "court": 1
            },
            "limit": None
        }
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_date_range_with_limit(self):
        """Test get_positions_by_date_range with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_date_range("2023-01-01", "2023-12-31", limit=10)
        
        expected_params = {
            "page": 1,
            "filters": {
                "date_start__gte": "2023-01-01",
                "date_start__lte": "2023-12-31"
            },
            "limit": 10
        }
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_nomination_process_basic(self):
        """Test get_positions_by_nomination_process without limit."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_nomination_process("presidential")
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"nomination_process": "presidential"}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_nomination_process_with_limit(self):
        """Test get_positions_by_nomination_process with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_nomination_process("presidential", limit=10)
        
        expected_params = {"page": 1, "filters": {"nomination_process": "presidential"}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_supervisor_basic(self):
        """Test get_positions_by_supervisor without limit."""
        mock_response = {"results": [{"id": 1, "position_type": "mag"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_supervisor(1)
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"supervisor": 1}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_supervisor_with_limit(self):
        """Test get_positions_by_supervisor with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_supervisor(1, limit=10)
        
        expected_params = {"page": 1, "filters": {"supervisor": 1}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_jurisdiction_basic(self):
        """Test get_positions_by_jurisdiction without limit."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_positions_by_jurisdiction("F")
        
        assert len(result) == 1
        expected_params = {"page": 1, "filters": {"court__jurisdiction": "F"}, "limit": None}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_positions_by_jurisdiction_with_limit(self):
        """Test get_positions_by_jurisdiction with limit."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        self.api.get_positions_by_jurisdiction("S", limit=10)
        
        expected_params = {"page": 1, "filters": {"court__jurisdiction": "S"}, "limit": 10}
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_current_position_for_judge_found(self):
        """Test get_current_position_for_judge when position is found."""
        mock_response = {"results": [{"id": 1, "position_type": "jud"}]}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_current_position_for_judge(1)
        
        assert isinstance(result, Position)
        expected_params = {
            "page": 1,
            "filters": {
                "judge": 1,
                "date_termination__isnull": True
            },
            "limit": 1
        }
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_get_current_position_for_judge_not_found(self):
        """Test get_current_position_for_judge when no position is found."""
        mock_response = {"results": []}
        self.mock_client.get.return_value = mock_response
        
        result = self.api.get_current_position_for_judge(1)
        
        assert result is None
        expected_params = {
            "page": 1,
            "filters": {
                "judge": 1,
                "date_termination__isnull": True
            },
            "limit": 1
        }
        self.mock_client.get.assert_called_once_with("/positions/", params=expected_params)
    
    def test_error_handling_court_listener_error(self):
        """Test error handling for CourtListenerError."""
        self.mock_client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.api.list_positions()
    
    def test_error_handling_network_error(self):
        """Test error handling for network errors."""
        self.mock_client.get.side_effect = Exception("Network Error")
        
        with pytest.raises(Exception):
            self.api.get_position(1)
