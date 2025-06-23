import os
import pytest
from courtlistener.client import CourtListenerClient

pytestmark = pytest.mark.integration

API_TOKEN = os.environ.get('COURTLISTENER_API_TOKEN')

@pytest.fixture(scope='module')
def client():
    if not API_TOKEN:
        pytest.skip('No API token set for integration tests')
    return CourtListenerClient(api_key=API_TOKEN)

class TestCourtsIntegration:
    """Integration tests for Courts API."""
    
    def test_list_courts(self, client):
        """Test listing courts."""
        resp = client.courts.list_courts(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_court(self, client):
        """Test getting a specific court."""
        # First get a list to find a valid court ID
        resp = client.courts.list_courts(page=1)
        if resp['results']:
            court_id = resp['results'][0]['id']
            detail = client.courts.get_court(court_id)
            assert detail['id'] == court_id
    
    def test_get_court_by_url(self, client):
        """Test getting a court by URL."""
        detail = client.courts.get_court_by_url('scotus')
        assert detail['url'] == 'scotus'
    
    def test_get_federal_courts(self, client):
        """Test getting federal courts."""
        resp = client.courts.get_federal_courts()
        assert 'results' in resp
        for court in resp['results']:
            assert court['jurisdiction'] == 'F'
    
    def test_get_state_courts(self, client):
        """Test getting state courts."""
        resp = client.courts.get_state_courts()
        assert 'results' in resp
        for court in resp['results']:
            assert court['jurisdiction'] == 'S'
    
    def test_get_court_opinions(self, client):
        """Test getting opinions for a court."""
        resp = client.courts.get_court_opinions(1)  # SCOTUS
        assert 'results' in resp
    
    def test_get_court_dockets(self, client):
        """Test getting dockets for a court."""
        resp = client.courts.get_court_dockets(1)  # SCOTUS
        assert 'results' in resp

class TestJudgesIntegration:
    """Integration tests for Judges API."""
    
    def test_list_judges(self, client):
        """Test listing judges."""
        resp = client.judges.list_judges(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_judge(self, client):
        """Test getting a specific judge."""
        resp = client.judges.list_judges(page=1)
        if resp['results']:
            judge_id = resp['results'][0]['id']
            detail = client.judges.get_judge(judge_id)
            assert detail['id'] == judge_id
    
    def test_search_judges(self, client):
        """Test searching judges."""
        resp = client.judges.search_judges(q='Roberts')
        assert 'results' in resp

class TestPartiesIntegration:
    """Integration tests for Parties API."""
    
    def test_list_parties(self, client):
        """Test listing parties."""
        resp = client.parties.list_parties(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_party(self, client):
        """Test getting a specific party."""
        resp = client.parties.list_parties(page=1)
        if resp['results']:
            party_id = resp['results'][0]['id']
            detail = client.parties.get_party(party_id)
            assert detail['id'] == party_id
    
    def test_search_parties(self, client):
        """Test searching parties."""
        resp = client.parties.search_parties(q='Smith')
        assert 'results' in resp

class TestAttorneysIntegration:
    """Integration tests for Attorneys API."""
    
    def test_list_attorneys(self, client):
        """Test listing attorneys."""
        resp = client.attorneys.list_attorneys(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_attorney(self, client):
        """Test getting a specific attorney."""
        resp = client.attorneys.list_attorneys(page=1)
        if resp['results']:
            attorney_id = resp['results'][0]['id']
            detail = client.attorneys.get_attorney(attorney_id)
            assert detail['id'] == attorney_id
    
    def test_search_attorneys(self, client):
        """Test searching attorneys."""
        resp = client.attorneys.search_attorneys(q='Smith')
        assert 'results' in resp

class TestDocumentsIntegration:
    """Integration tests for Documents API."""
    
    def test_list_documents(self, client):
        """Test listing documents."""
        resp = client.documents.list_documents(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_document(self, client):
        """Test getting a specific document."""
        resp = client.documents.list_documents(page=1)
        if resp['results']:
            doc_id = resp['results'][0]['id']
            detail = client.documents.get_document(doc_id)
            assert detail['id'] == doc_id
    
    def test_search_documents(self, client):
        """Test searching documents."""
        resp = client.documents.search_documents(q='motion')
        assert 'results' in resp

class TestAudioIntegration:
    """Integration tests for Audio API."""
    
    def test_list_audio(self, client):
        """Test listing audio."""
        resp = client.audio.list_audio(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_audio(self, client):
        """Test getting a specific audio."""
        resp = client.audio.list_audio(page=1)
        if resp['results']:
            audio_id = resp['results'][0]['id']
            detail = client.audio.get_audio(audio_id)
            assert detail['id'] == audio_id
    
    def test_search_audio(self, client):
        """Test searching audio."""
        resp = client.audio.search_audio(source='oral_argument')
        assert 'results' in resp

class TestFinancialIntegration:
    """Integration tests for Financial API."""
    
    def test_list_financial(self, client):
        """Test listing financial records."""
        resp = client.financial.list_financial(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_financial(self, client):
        """Test getting a specific financial record."""
        resp = client.financial.list_financial(page=1)
        if resp['results']:
            financial_id = resp['results'][0]['id']
            detail = client.financial.get_financial(financial_id)
            assert detail['id'] == financial_id
    
    def test_search_financial(self, client):
        """Test searching financial records."""
        resp = client.financial.search_financial(type='filing_fee')
        assert 'results' in resp

class TestCitationsIntegration:
    """Integration tests for Citations API."""
    
    def test_list_citations(self, client):
        """Test listing citations."""
        resp = client.citations.list_citations(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_citation(self, client):
        """Test getting a specific citation."""
        resp = client.citations.list_citations(page=1)
        if resp['results']:
            citation_id = resp['results'][0]['id']
            detail = client.citations.get_citation(citation_id)
            assert detail['id'] == citation_id
    
    def test_search_citations(self, client):
        """Test searching citations."""
        resp = client.citations.search_citations(type='federal')
        assert 'results' in resp

class TestDocketEntriesIntegration:
    """Integration tests for Docket Entries API."""
    
    def test_list_docket_entries(self, client):
        """Test listing docket entries."""
        resp = client.docket_entries.list_docket_entries(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_docket_entry(self, client):
        """Test getting a specific docket entry."""
        resp = client.docket_entries.list_docket_entries(page=1)
        if resp['results']:
            entry_id = resp['results'][0]['id']
            detail = client.docket_entries.get_docket_entry(entry_id)
            assert detail['id'] == entry_id
    
    def test_search_docket_entries(self, client):
        """Test searching docket entries."""
        resp = client.docket_entries.search_docket_entries(entry_number=1)
        assert 'results' in resp

class TestOpinionClustersIntegration:
    """Integration tests for Opinion Clusters API."""
    
    def test_list_opinion_clusters(self, client):
        """Test listing opinion clusters."""
        resp = client.opinion_clusters.list_opinion_clusters(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_opinion_cluster(self, client):
        """Test getting a specific opinion cluster."""
        resp = client.opinion_clusters.list_opinion_clusters(page=1)
        if resp['results']:
            cluster_id = resp['results'][0]['id']
            detail = client.opinion_clusters.get_opinion_cluster(cluster_id)
            assert detail['id'] == cluster_id
    
    def test_search_opinion_clusters(self, client):
        """Test searching opinion clusters."""
        resp = client.opinion_clusters.search_opinion_clusters(q='Miranda')
        assert 'results' in resp

class TestPositionsIntegration:
    """Integration tests for Positions API."""
    
    def test_list_positions(self, client):
        """Test listing positions."""
        resp = client.positions.list_positions(page=1)
        assert 'results' in resp
        assert isinstance(resp['results'], list)
    
    def test_get_position(self, client):
        """Test getting a specific position."""
        resp = client.positions.list_positions(page=1)
        if resp['results']:
            position_id = resp['results'][0]['id']
            detail = client.positions.get_position(position_id)
            assert detail['id'] == position_id
    
    def test_search_positions(self, client):
        """Test searching positions."""
        resp = client.positions.search_positions(title='Judge')
        assert 'results' in resp

class TestAdvancedIntegration:
    """Advanced integration tests for complex workflows."""
    
    def test_multi_endpoint_workflow(self, client):
        """Test a complex workflow across multiple endpoints."""
        # 1. Search for opinions
        opinions = client.search.search_opinions(q='Miranda', court='scotus')
        if opinions['results']:
            opinion = opinions['results'][0]
            
            # 2. Get opinion details
            opinion_detail = client.opinions.get_opinion(opinion['id'])
            assert opinion_detail['id'] == opinion['id']
            
            # 3. Get opinion cluster
            if opinion_detail.get('cluster'):
                cluster = client.opinion_clusters.get_opinion_cluster(opinion_detail['cluster'])
                assert cluster['id'] == opinion_detail['cluster']
                
                # 4. Get opinions in cluster
                cluster_opinions = client.opinion_clusters.get_opinions_in_cluster(cluster['id'])
                assert 'results' in cluster_opinions
    
    def test_large_pagination_scenario(self, client):
        """Test pagination with large result sets."""
        # Get first page
        page1 = client.dockets.list_dockets(page=1, page_size=100)
        assert 'results' in page1
        
        # Get second page
        page2 = client.dockets.list_dockets(page=2, page_size=100)
        assert 'results' in page2
        
        # Ensure pages are different
        if page1['results'] and page2['results']:
            assert page1['results'][0]['id'] != page2['results'][0]['id']
    
    def test_complex_filter_combinations(self, client):
        """Test complex filter combinations."""
        resp = client.search.search_opinions(
            q='Miranda',
            court='scotus',
            type='010combined',
            date_filed_min='2000-01-01',
            date_filed_max='2020-12-31'
        )
        assert 'results' in resp
    
    def test_data_consistency_across_endpoints(self, client):
        """Test data consistency across related endpoints."""
        # Get a docket
        dockets = client.dockets.list_dockets(page=1)
        if dockets['results']:
            docket = dockets['results'][0]
            
            # Get docket details
            docket_detail = client.dockets.get_docket(docket['id'])
            assert docket_detail['id'] == docket['id']
            
            # Get docket entries
            entries = client.dockets.get_docket_entries(docket['id'])
            assert 'results' in entries
            
            # Get docket documents
            documents = client.dockets.get_documents(docket['id'])
            assert 'results' in documents
            
            # Get docket parties
            parties = client.dockets.get_parties(docket['id'])
            assert 'results' in parties 