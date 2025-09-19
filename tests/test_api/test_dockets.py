import pytest
from unittest.mock import Mock, patch
from courtlistener.api.dockets import DocketsAPI
from courtlistener.models.docket import Docket
from courtlistener.exceptions import CourtListenerError


class TestDocketsAPI:
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.dockets_api = DocketsAPI(self.client)
    
    def test_get_docket(self):
        """Test getting a single docket."""
        mock_response = {
            'id': 1,
            'docket_number': '21-123',
            'case_name': 'Smith v. Jones',
            'court': 1
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_docket(1)
        
        self.client.get.assert_called_once_with('dockets/1/')
        assert isinstance(result, Docket)
        assert result.id == 1
    
    def test_list_dockets(self):
        """Test listing dockets."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'docket_number': '21-123'},
                {'id': 2, 'docket_number': '21-124'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.list_dockets(
            court='scotus',
            date_filed_min='2020-01-01',
            page=1
        )
        
        self.client.get.assert_called_once_with(
            'dockets/',
            params={
                'page': 1,
                'court': 'scotus',
                'date_filed_min': '2020-01-01'
            }
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Docket)
        assert result[0].id == 1
    
    def test_list_dockets_with_filters(self):
        """Test listing dockets with filters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        filters = {
            'nature_of_suit': 'Civil Rights',
            'jurisdiction_type': 'Federal Question'
        }
        
        result = self.dockets_api.list_dockets(filters=filters)
        
        self.client.get.assert_called_once_with(
            'dockets/',
            params={'page': 1, 'filters': filters}
        )
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_get_docket_entries(self):
        """Test getting docket entries for a docket."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'entry_number': 1}]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_docket_entries(1)
        
        self.client.get.assert_called_once_with('docket-entries/', params={'docket': 1, 'page': 1})
        assert isinstance(result, dict)
        assert result['count'] == 1
    
    def test_get_docket_entries_with_params(self):
        """Test getting docket entries with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_docket_entries(
            1,
            entry_number=1,
            date_filed_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            'docket-entries/',
            params={
                'docket': 1,
                'page': 1,
                'entry_number': 1,
                'date_filed_min': '2020-01-01'
            }
        )
        assert isinstance(result, dict)
        assert result['count'] == 0
    
    def test_get_documents(self):
        """Test getting documents for a docket."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'document_type': 'motion'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_documents(1)
        
        self.client.get.assert_called_once_with('documents/', params={'docket': 1, 'page': 1})
        assert isinstance(result, dict)
        assert result['count'] == 1
    
    def test_get_documents_with_params(self):
        """Test getting documents with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_documents(
            1,
            document_type='motion',
            date_filed_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            'documents/',
            params={
                'docket': 1,
                'page': 1,
                'document_type': 'motion',
                'date_filed_min': '2020-01-01'
            }
        )
        assert isinstance(result, dict)
        assert result['count'] == 0
    
    def test_get_parties(self):
        """Test getting parties for a docket."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'name': 'John Smith', 'type': 'plaintiff'},
                {'id': 2, 'name': 'Jane Doe', 'type': 'defendant'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_parties(1)
        
        self.client.get.assert_called_once_with('parties/', params={'docket': 1, 'page': 1})
        assert isinstance(result, dict)
        assert result['count'] == 2
    
    def test_get_parties_with_params(self):
        """Test getting parties with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_parties(
            1,
            type='plaintiff',
            attorney=1
        )
        
        self.client.get.assert_called_once_with(
            'parties/',
            params={
                'docket': 1,
                'page': 1,
                'type': 'plaintiff',
                'attorney': 1
            }
        )
        assert isinstance(result, dict)
        assert result['count'] == 0
    
    def test_get_audio(self):
        """Test getting audio for a docket."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'source': 'oral_argument'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_audio(1)
        
        self.client.get.assert_called_once_with('audio/', params={'docket': 1, 'page': 1})
        assert isinstance(result, dict)
        assert result['count'] == 1
    
    def test_get_financial(self):
        """Test getting financial records for a docket."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'type': 'filing_fee', 'amount': 350.00}]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_financial(1)
        
        self.client.get.assert_called_once_with('financial-disclosures/', params={'docket': 1, 'page': 1})
        assert isinstance(result, dict)
        assert result['count'] == 1
    
    def test_error_handling(self):
        """Test error handling in docket methods."""
        self.client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.dockets_api.get_docket(1)
    
    def test_not_found_handling(self):
        """Test handling of not found dockets."""
        self.client.get.side_effect = CourtListenerError("Not found", status_code=404)
        
        with pytest.raises(CourtListenerError) as exc_info:
            self.dockets_api.get_docket(999)
        
        assert exc_info.value.status_code == 404
    
    def test_empty_docket_entries(self):
        """Test handling of empty docket entries."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_docket_entries(1)
        
        assert result['count'] == 0
        assert result['results'] == []
    
    def test_pagination_in_docket_entries(self):
        """Test pagination in docket entries."""
        mock_response = {
            'count': 50,
            'next': '/api/rest/v4/dockets/1/docket-entries/?page=2',
            'previous': None,
            'results': [{'id': 1, 'entry_number': 1}]
        }
        self.client.get.return_value = mock_response
        
        result = self.dockets_api.get_docket_entries(1, page=1)
        
        self.client.get.assert_called_once_with(
            'docket-entries/',
            params={'docket': 1, 'page': 1}
        )
        assert isinstance(result, dict)
        assert result['count'] == 50
        assert result['next'] is not None 