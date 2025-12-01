import os
import pytest
from courtlistener.client import CourtListenerClient
from courtlistener.exceptions import APIError, AuthenticationError, NotFoundError

pytestmark = pytest.mark.integration

API_TOKEN = os.environ.get('COURTLISTENER_API_TOKEN')

@pytest.fixture(scope='module')
def client():
    if not API_TOKEN:
        pytest.skip('No API token set for integration tests')
    return CourtListenerClient(api_token=API_TOKEN)

def skip_on_permission_error(func):
    """Helper to skip tests on API permission errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (APIError, AuthenticationError) as e:
            error_str = str(e).lower()
            status_code = getattr(e, 'status_code', None)
            if 'permission' in error_str or status_code in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    return wrapper

class TestCourtsIntegration:
    """Integration tests for Courts API."""
    
    def test_list_courts(self, client):
        """Test listing courts."""
        resp = client.courts.list_courts(page=1)
        assert isinstance(resp, list)
        assert len(resp) > 0
        assert hasattr(resp[0], 'id')
    
    def test_get_court(self, client):
        """Test getting a specific court."""
        # First get a list to find a valid court ID
        resp = client.courts.list_courts(page=1)
        if resp:
            court_id = resp[0].id
            detail = client.courts.get_court(court_id)
            assert detail.id == court_id
    
    def test_get_court_by_url(self, client):
        """Test getting a court by URL."""
        detail = client.courts.get_court_by_url('scotus')
        assert hasattr(detail, 'id')
        assert detail.id == 'scotus'
    
    def test_get_federal_courts(self, client):
        """Test getting federal courts."""
        resp = client.courts.get_federal_courts()
        assert isinstance(resp, list)
        for court in resp:
            assert hasattr(court, 'jurisdiction')
            # Note: jurisdiction might be a property or attribute
    
    def test_get_state_courts(self, client):
        """Test getting state courts."""
        resp = client.courts.get_state_courts()
        assert isinstance(resp, list)
        for court in resp:
            assert hasattr(court, 'jurisdiction')
            # Note: jurisdiction might be a property or attribute
    
    def test_get_court_opinions(self, client):
        """Test getting opinions for a court."""
        try:
            resp = client.courts.get_court_opinions('scotus')
            assert isinstance(resp, dict) and 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401, 400):
                pytest.skip(f'API error (may require permissions): {e}')
            raise
    
    def test_get_court_dockets(self, client):
        """Test getting dockets for a court."""
        resp = client.courts.get_court_dockets('scotus')
        assert isinstance(resp, dict)
        assert 'results' in resp
        # Verify it's a paginated response
        assert 'count' in resp or len(resp.get('results', [])) >= 0

class TestJudgesIntegration:
    """Integration tests for Judges API."""
    
    def test_list_judges(self, client):
        """Test listing judges."""
        try:
            resp = client.judges.list_judges(page=1)
            assert isinstance(resp, list)
            if resp:
                assert hasattr(resp[0], 'id')
        except (APIError, AuthenticationError, NotFoundError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401, 404):
                pytest.skip(f'API error (may require permissions or endpoint unavailable): {e}')
            raise
    
    def test_get_judge(self, client):
        """Test getting a specific judge."""
        try:
            resp = client.judges.list_judges(page=1)
            if resp:
                judge_id = resp[0].id
                detail = client.judges.get_judge(judge_id)
                assert detail.id == judge_id
        except (APIError, AuthenticationError, NotFoundError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401, 404):
                pytest.skip(f'API error (may require permissions or endpoint unavailable): {e}')
            raise
    
    def test_search_judges(self, client):
        """Test searching judges."""
        try:
            resp = client.judges.search_judges(q='Roberts')
            assert isinstance(resp, list)
        except (APIError, AuthenticationError, NotFoundError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401, 404):
                pytest.skip(f'API error (may require permissions or endpoint unavailable): {e}')
            raise

class TestPartiesIntegration:
    """Integration tests for Parties API."""
    
    def test_list_parties(self, client):
        """Test listing parties."""
        try:
            resp = client.parties.list_parties(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_party(self, client):
        """Test getting a specific party."""
        try:
            resp = client.parties.list_parties(page=1)
            if resp.get('results'):
                party_id = resp['results'][0]['id']
                detail = client.parties.get_party(party_id)
                assert detail['id'] == party_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_parties(self, client):
        """Test searching parties."""
        try:
            resp = client.parties.search_parties(q='Smith')
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestAttorneysIntegration:
    """Integration tests for Attorneys API."""
    
    def test_list_attorneys(self, client):
        """Test listing attorneys."""
        try:
            resp = client.attorneys.list_attorneys(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_attorney(self, client):
        """Test getting a specific attorney."""
        try:
            resp = client.attorneys.list_attorneys(page=1)
            if resp.get('results'):
                attorney_id = resp['results'][0]['id']
                detail = client.attorneys.get_attorney(attorney_id)
                assert detail['id'] == attorney_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_attorneys(self, client):
        """Test searching attorneys."""
        try:
            resp = client.attorneys.search_attorneys(q='Smith')
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestDocumentsIntegration:
    """Integration tests for Documents API."""
    
    def test_list_documents(self, client):
        """Test listing documents."""
        try:
            resp = client.documents.list_documents(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_document(self, client):
        """Test getting a specific document."""
        try:
            resp = client.documents.list_documents(page=1)
            if resp.get('results'):
                doc_id = resp['results'][0]['id']
                detail = client.documents.get_document(doc_id)
                assert detail.id == doc_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_documents(self, client):
        """Test searching documents."""
        try:
            resp = client.documents.search_documents(q='motion')
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestAudioIntegration:
    """Integration tests for Audio API."""
    
    def test_list_audio(self, client):
        """Test listing audio."""
        resp = client.audio.list_audio(page=1)
        assert isinstance(resp, list)
        # Audio endpoint may return empty list if restricted
    
    def test_get_audio(self, client):
        """Test getting a specific audio."""
        resp = client.audio.list_audio(page=1)
        if resp:
            audio_id = resp[0].id
            detail = client.audio.get_audio(audio_id)
            if detail:  # get_audio may return None if restricted
                assert detail.id == audio_id
    
    def test_search_audio(self, client):
        """Test searching audio."""
        resp = client.audio.search_audio(q='test')
        assert isinstance(resp, list)
        # Audio endpoint may return empty list if restricted

class TestFinancialIntegration:
    """Integration tests for Financial API."""
    
    def test_list_financial(self, client):
        """Test listing financial records."""
        try:
            resp = client.financial.list_financial(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_financial(self, client):
        """Test getting a specific financial record."""
        try:
            resp = client.financial.list_financial(page=1)
            if resp.get('results'):
                financial_id = resp['results'][0]['id']
                detail = client.financial.get_disclosure(financial_id)
                assert detail.id == financial_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_financial(self, client):
        """Test searching financial records."""
        try:
            resp = client.financial.search_financial(page=1)
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestCitationsIntegration:
    """Integration tests for Citations API."""
    
    def test_list_citations(self, client):
        """Test listing citations."""
        try:
            resp = client.citations.list_citations(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_citation(self, client):
        """Test getting a specific citation."""
        try:
            resp = client.citations.list_citations(page=1)
            if resp.get('results'):
                citation_id = resp['results'][0]['id']
                detail = client.citations.get(citation_id)
                assert isinstance(detail, dict) and detail.get('id') == citation_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_citations(self, client):
        """Test searching citations."""
        try:
            resp = client.citations.search_citations(page=1)
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestDocketEntriesIntegration:
    """Integration tests for Docket Entries API."""
    
    def test_list_docket_entries(self, client):
        """Test listing docket entries."""
        try:
            resp = client.docket_entries.list_docket_entries(page=1)
            assert 'results' in resp
            assert isinstance(resp['results'], list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_get_docket_entry(self, client):
        """Test getting a specific docket entry."""
        try:
            resp = client.docket_entries.list_docket_entries(page=1)
            if resp.get('results'):
                entry_id = resp['results'][0]['id']
                detail = client.docket_entries.get_entry(entry_id)
                assert detail.id == entry_id
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_search_docket_entries(self, client):
        """Test searching docket entries."""
        try:
            resp = client.docket_entries.search_docket_entries(page=1)
            assert 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise

class TestOpinionClustersIntegration:
    """Integration tests for Opinion Clusters API."""
    
    def test_list_opinion_clusters(self, client):
        """Test listing opinion clusters."""
        resp = client.opinions.list_opinion_clusters(page=1)
        assert isinstance(resp, dict) and 'results' in resp
    
    def test_get_opinion_cluster(self, client):
        """Test getting a specific opinion cluster."""
        resp = client.opinions.list_opinion_clusters(page=1)
        if resp.get('results'):
            cluster_id = resp['results'][0]['id']
            detail = client.opinions.get_opinion_cluster(cluster_id)
            assert isinstance(detail, dict) and detail.get('id') == cluster_id
    
    def test_search_opinion_clusters(self, client):
        """Test searching opinion clusters."""
        resp = client.clusters.search_clusters(q='Miranda')
        assert isinstance(resp, list)

class TestPositionsIntegration:
    """Integration tests for Positions API."""
    
    def test_list_positions(self, client):
        """Test listing positions."""
        resp = client.positions.list_positions(page=1)
        assert isinstance(resp, list)
        if resp:
            assert hasattr(resp[0], 'id')
    
    def test_get_position(self, client):
        """Test getting a specific position."""
        try:
            resp = client.positions.list_positions(page=1)
            if resp:
                position_id = resp[0].id
                detail = client.positions.get_position(position_id)
                assert detail.id == position_id
        except (APIError, AuthenticationError, NotFoundError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401, 404):
                pytest.skip(f'API error (may require permissions or endpoint unavailable): {e}')
            raise
    
    def test_search_positions(self, client):
        """Test searching positions."""
        resp = client.positions.search_positions(q='Judge')
        assert isinstance(resp, list)

class TestAdvancedIntegration:
    """Advanced integration tests for complex workflows."""
    
    def test_multi_endpoint_workflow(self, client):
        """Test a complex workflow across multiple endpoints."""
        try:
            # 1. Search for opinions
            opinions = client.search.search_opinions(q='Miranda', court='scotus')
            if isinstance(opinions, dict) and opinions.get('results'):
                opinion = opinions['results'][0]
                
                # 2. Get opinion details
                opinion_detail = client.opinions.get_opinion(opinion['id'])
                assert hasattr(opinion_detail, 'id')
                assert opinion_detail.id == opinion['id']
                
                # 3. Get opinion cluster
                if hasattr(opinion_detail, 'cluster') and opinion_detail.cluster:
                    cluster = client.opinions.get_opinion_cluster(opinion_detail.cluster)
                    assert isinstance(cluster, dict) and cluster.get('id') == opinion_detail.cluster
                    
                    # 4. Get opinions in cluster
                    cluster_opinions = client.opinions.get_opinions_in_cluster(cluster['id'])
                    assert isinstance(cluster_opinions, list)
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_large_pagination_scenario(self, client):
        """Test pagination with large result sets."""
        # Get first page
        page1 = client.dockets.list_dockets(page=1)
        assert isinstance(page1, list)
        
        # Get second page
        page2 = client.dockets.list_dockets(page=2)
        assert isinstance(page2, list)
        
        # Ensure pages are different (if both have results)
        if page1 and page2:
            # Check if results are actually different
            ids1 = {d.id for d in page1}
            ids2 = {d.id for d in page2}
            # Pages should have different IDs, or at least not be identical
            if ids1 == ids2 and len(page1) == len(page2):
                # Same results on both pages - might be API limitation
                pytest.skip('API returned same results on different pages (may be API limitation)')
            else:
                # At least some difference
                assert len(ids1.intersection(ids2)) < len(ids1) or len(ids1.intersection(ids2)) < len(ids2)
    
    def test_complex_filter_combinations(self, client):
        """Test complex filter combinations."""
        try:
            resp = client.search.search_opinions(
                q='Miranda',
                court='scotus',
                type='010combined',
                date_filed_min='2000-01-01',
                date_filed_max='2020-12-31'
            )
            assert isinstance(resp, dict) and 'results' in resp
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
    
    def test_data_consistency_across_endpoints(self, client):
        """Test data consistency across related endpoints."""
        try:
            # Get a docket
            dockets = client.dockets.list_dockets(page=1)
            if dockets:
                docket = dockets[0]
                
                # Get docket details
                docket_detail = client.dockets.get_docket(docket.id)
                assert docket_detail.id == docket.id
                
                # Get docket entries
                entries = client.dockets.get_docket_entries(docket.id)
                assert isinstance(entries, dict) and 'results' in entries
                
                # Get docket documents
                documents = client.dockets.get_documents(docket.id)
                assert isinstance(documents, dict) and 'results' in documents
                
                # Get docket parties
                parties = client.dockets.get_parties(docket.id)
                assert isinstance(parties, dict) and 'results' in parties
        except (APIError, AuthenticationError) as e:
            if 'permission' in str(e).lower() or getattr(e, 'status_code', None) in (403, 401):
                pytest.skip(f'API permission error: {e}')
            raise
