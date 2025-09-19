import pytest
from unittest.mock import Mock, patch
from courtlistener.api.opinions import OpinionsAPI
from courtlistener.models.opinion import Opinion
from courtlistener.exceptions import CourtListenerError


class TestOpinionsAPI:
    def setup_method(self):
        """Set up test fixtures."""
        self.client = Mock()
        self.opinions_api = OpinionsAPI(self.client)
    
    def test_get_opinion(self):
        """Test getting a single opinion."""
        mock_response = {
            'id': 1,
            'cluster': 1,
            'author': 1,
            'type': '010combined',
            'type_name': 'Majority Opinion'
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_opinion(1)
        
        self.client.get.assert_called_once_with('/opinions/1/')
        assert isinstance(result, Opinion)
        assert result.id == 1
        assert result.type == '010combined'
    
    def test_list_opinions(self):
        """Test listing opinions."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'type': '010combined'},
                {'id': 2, 'type': '020concurring'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.list_opinions(
            court='scotus',
            type='010combined',
            page=1
        )
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={
                'court': 'scotus',
                'type': '010combined',
                'page': 1
            }
        )
        assert isinstance(result, list)
        assert len(result) == 2
        assert isinstance(result[0], Opinion)
        assert result[0].id == 1
        assert result[1].id == 2
    
    def test_list_opinions_with_filters(self):
        """Test listing opinions with filters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        filters = {
            'author': 1,
            'joined_by': [2, 3],
            'date_filed_min': '2020-01-01'
        }
        
        result = self.opinions_api.list_opinions(filters=filters)
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={'page': 1, 'author': 1, 'joined_by': [2, 3], 'date_filed_min': '2020-01-01'}
        )
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_get_opinion_cluster(self):
        """Test getting an opinion cluster."""
        mock_response = {
            'id': 1,
            'case_name': 'Smith v. Jones',
            'case_name_short': 'Smith',
            'date_filed': '2020-01-01T00:00:00Z'
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_opinion_cluster(1)
        
        self.client.get.assert_called_once_with('/clusters/1/')
        assert isinstance(result, dict)
        assert result['id'] == 1
    
    def test_list_opinion_clusters(self):
        """Test listing opinion clusters."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'case_name': 'Smith v. Jones'},
                {'id': 2, 'case_name': 'Doe v. Roe'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.list_opinion_clusters(
            court='scotus',
            date_filed_min='2020-01-01'
        )
        
        self.client.get.assert_called_once_with(
            '/clusters/',
            params={
                'page': 1,
                'court': 'scotus',
                'date_filed_min': '2020-01-01'
            }
        )
        assert isinstance(result, dict)
        assert result['count'] == 2
    
    def test_get_opinions_in_cluster(self):
        """Test getting opinions in a cluster."""
        mock_response = {
            'count': 2,
            'results': [
                {'id': 1, 'type': '010combined'},
                {'id': 2, 'type': '020concurring'}
            ]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_opinions_in_cluster(1)
        
        self.client.get.assert_called_once_with('/opinions/', params={'cluster': 1})
        assert isinstance(result, list)
        assert len(result) == 2
    
    def test_get_opinions_in_cluster_with_params(self):
        """Test getting opinions in a cluster with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_opinions_in_cluster(
            1,
            type='010combined',
            author=1
        )
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={
                'cluster': 1,
                'type': '010combined',
                'author': 1
            }
        )
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_get_citations(self):
        """Test getting citations for an opinion."""
        mock_response = {
            'count': 1,
            'results': [{'id': 1, 'volume': 410, 'reporter': 'U.S.', 'page': 113}]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_citations(1)
        
        self.client.get.assert_called_once_with('/opinions-cited/', params={'citing_opinion': 1})
        assert isinstance(result, dict)
        assert result['count'] == 1
    
    def test_get_citations_with_params(self):
        """Test getting citations with parameters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_citations(
            1,
            type='federal',
            year=1973
        )
        
        self.client.get.assert_called_once_with(
            '/opinions-cited/',
            params={
                'citing_opinion': 1,
                'type': 'federal',
                'year': 1973
            }
        )
        assert isinstance(result, dict)
        assert result['count'] == 0
    
    def test_get_sub_opinions(self):
        """Test getting sub-opinions for an opinion."""
        mock_response = {
            'count': 1,
            'results': [{'id': 2, 'type': '020concurring'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_sub_opinions(1)
        
        self.client.get.assert_called_once_with('/opinions/', params={'parent_opinion': 1})
        assert isinstance(result, list)
        assert len(result) == 1
    
    def test_error_handling(self):
        """Test error handling in opinion methods."""
        self.client.get.side_effect = CourtListenerError("API Error")
        
        with pytest.raises(CourtListenerError):
            self.opinions_api.get_opinion(1)
    
    def test_not_found_handling(self):
        """Test handling of not found opinions."""
        self.client.get.side_effect = CourtListenerError("Not found", status_code=404)
        
        with pytest.raises(CourtListenerError) as exc_info:
            self.opinions_api.get_opinion(999)
        
        assert exc_info.value.status_code == 404
    
    def test_empty_opinion_cluster(self):
        """Test handling of empty opinion clusters."""
        mock_response = {'count': 0, 'results': []}
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.get_opinions_in_cluster(1)
        
        assert isinstance(result, list)
        assert len(result) == 0
    
    def test_pagination_in_opinions(self):
        """Test pagination in opinions."""
        mock_response = {
            'count': 100,
            'next': '/api/rest/v4/opinions/?page=2',
            'previous': None,
            'results': [{'id': 1, 'type': '010combined'}]
        }
        self.client.get.return_value = mock_response
        
        result = self.opinions_api.list_opinions(page=1)
        
        self.client.get.assert_called_once_with(
            '/opinions/',
            params={'page': 1}
        )
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Opinion)
        assert result[0].id == 1
    
    def test_opinion_types(self):
        """Test filtering by opinion types."""
        mock_response = {'count': 1, 'results': [{'id': 1, 'type': '010combined'}]}
        self.client.get.return_value = mock_response
        
        # Test majority opinions
        result = self.opinions_api.list_opinions(type='010combined')
        self.client.get.assert_called_with('/opinions/', params={'page': 1, 'type': '010combined'})
        
        # Test concurring opinions
        result = self.opinions_api.list_opinions(type='020concurring')
        self.client.get.assert_called_with('/opinions/', params={'page': 1, 'type': '020concurring'})
        
        # Test dissenting opinions
        result = self.opinions_api.list_opinions(type='030dissenting')
        self.client.get.assert_called_with('/opinions/', params={'page': 1, 'type': '030dissenting'}) 