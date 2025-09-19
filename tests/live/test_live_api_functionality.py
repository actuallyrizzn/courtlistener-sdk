"""
Live API tests for specific functionality and data validation.
These tests require a valid API token and will make real API calls.
"""

import pytest
import os
from courtlistener import CourtListenerClient
from courtlistener.exceptions import CourtListenerError


class TestLiveAPIFunctionality:
    """Live API tests for specific functionality."""
    
    @classmethod
    def setup_class(cls):
        """Set up test class with API token."""
        api_token = os.getenv('COURTLISTENER_API_TOKEN')
        if not api_token:
            pytest.skip("COURTLISTENER_API_TOKEN environment variable not set")
        
        cls.client = CourtListenerClient(api_token=api_token)
    
    def test_search_functionality(self):
        """Test search functionality with various queries."""
        # Test basic search
        result = self.client.search.list(q="constitutional law", page_size=5)
        assert 'count' in result
        assert 'results' in result
        
        # Test search with court filter
        result = self.client.search.list(
            q="constitutional",
            court="scotus",
            page_size=5
        )
        assert 'count' in result
        assert 'results' in result
        
        # Test search with date filter
        result = self.client.search.list(
            q="constitutional",
            date_filed__gte="2020-01-01",
            page_size=5
        )
        assert 'count' in result
        assert 'results' in result
    
    def test_opinion_citations(self):
        """Test opinion citations functionality."""
        # Get an opinion first
        opinions = self.client.opinions.list(page_size=1)
        if opinions['results']:
            opinion_id = opinions['results'][0]['id']
            
            # Test getting citations for this opinion
            citations = self.client.opinions_cited.list(
                citing_opinion=opinion_id,
                page_size=5
            )
            assert 'count' in citations
            assert 'results' in citations
    
    def test_financial_disclosures_workflow(self):
        """Test financial disclosures workflow."""
        # Get a judge first
        judges = self.client.judges.list(page_size=1)
        if judges['results']:
            judge_id = judges['results'][0]['id']
            
            # Test getting financial disclosures
            disclosures = self.client.financial_disclosures.list(
                judge=judge_id,
                page_size=5
            )
            assert 'count' in disclosures
            assert 'results' in disclosures
            
            if disclosures['results']:
                disclosure_id = disclosures['results'][0]['id']
                
                # Test getting investments
                investments = self.client.investments.list(
                    financial_disclosure=disclosure_id,
                    page_size=5
                )
                assert 'count' in investments
                assert 'results' in investments
                
                # Test getting gifts
                gifts = self.client.gifts.list(
                    financial_disclosure=disclosure_id,
                    page_size=5
                )
                assert 'count' in gifts
                assert 'results' in gifts
    
    def test_people_and_education_workflow(self):
        """Test people and education workflow."""
        # Get people
        people = self.client.people.list(page_size=1)
        if people['results']:
            person_id = people['results'][0]['id']
            
            # Test getting education records
            educations = self.client.educations.list(
                person=person_id,
                page_size=5
            )
            assert 'count' in educations
            assert 'results' in educations
            
            # Test getting ABA ratings
            ratings = self.client.aba_ratings.list(
                person=person_id,
                page_size=5
            )
            assert 'count' in ratings
            assert 'results' in ratings
            
            # Test getting political affiliations
            affiliations = self.client.political_affiliations.list(
                person=person_id,
                page_size=5
            )
            assert 'count' in affiliations
            assert 'results' in affiliations
    
    def test_docket_workflow(self):
        """Test docket workflow."""
        # Get a docket
        dockets = self.client.dockets.list(page_size=1)
        if dockets['results']:
            docket_id = dockets['results'][0]['id']
            
            # Test getting docket entries
            entries = self.client.docket_entries.list(
                docket=docket_id,
                page_size=5
            )
            assert 'count' in entries
            assert 'results' in entries
            
            # Test getting parties
            parties = self.client.parties.list(
                docket=docket_id,
                page_size=5
            )
            assert 'count' in parties
            assert 'results' in parties
            
            # Test getting attorneys
            attorneys = self.client.attorneys.list(
                docket=docket_id,
                page_size=5
            )
            assert 'count' in attorneys
            assert 'results' in attorneys
    
    def test_recap_documents_workflow(self):
        """Test RECAP documents workflow."""
        # Get RECAP documents
        documents = self.client.recap_documents.list(page_size=5)
        assert 'count' in documents
        assert 'results' in documents
        
        if documents['results']:
            doc = documents['results'][0]
            assert 'id' in doc
            assert 'file_url' in doc or 'docket' in doc
    
    def test_audio_workflow(self):
        """Test audio workflow."""
        # Get audio recordings
        audio = self.client.audio.list(page_size=5)
        assert 'count' in audio
        assert 'results' in audio
        
        if audio['results']:
            recording = audio['results'][0]
            assert 'id' in recording
            assert 'file_url' in recording or 'docket' in recording
    
    def test_alerts_functionality(self):
        """Test alerts functionality (if available)."""
        # Test listing alerts
        alerts = self.client.alerts.list(page_size=5)
        assert 'count' in alerts
        assert 'results' in alerts
        
        # Test listing docket alerts
        docket_alerts = self.client.docket_alerts.list(page_size=5)
        assert 'count' in docket_alerts
        assert 'results' in docket_alerts
    
    def test_court_hierarchy(self):
        """Test court hierarchy and relationships."""
        # Get courts
        courts = self.client.courts.list(page_size=10)
        assert 'count' in courts
        assert 'results' in courts
        
        if courts['results']:
            # Test getting specific court
            court_id = courts['results'][0]['id']
            court = self.client.courts.get(court_id)
            assert court['id'] == court_id
            
            # Test getting opinions for this court
            opinions = self.client.opinions.list(
                court=court_id,
                page_size=5
            )
            assert 'count' in opinions
            assert 'results' in opinions
    
    def test_data_consistency(self):
        """Test data consistency across related endpoints."""
        # Get a docket
        dockets = self.client.dockets.list(page_size=1)
        if dockets['results']:
            docket = dockets['results'][0]
            docket_id = docket['id']
            
            # Get docket entries for this docket
            entries = self.client.docket_entries.list(
                docket=docket_id,
                page_size=5
            )
            
            # Verify that entries reference the correct docket
            for entry in entries['results']:
                if 'docket' in entry:
                    assert str(docket_id) in entry['docket']
    
    def test_pagination_consistency(self):
        """Test pagination consistency."""
        # Test that pagination works correctly
        page1 = self.client.opinions.list(page_size=2)
        assert 'count' in page1
        assert 'results' in page1
        assert len(page1['results']) <= 2
        
        if page1['next']:
            # Test that we can get the next page
            page2 = self.client.opinions.list(page_size=2, page=2)
            assert 'count' in page2
            assert 'results' in page2
            assert len(page2['results']) <= 2
            
            # Verify that results are different
            if page1['results'] and page2['results']:
                assert page1['results'][0]['id'] != page2['results'][0]['id']
    
    def test_filtering_accuracy(self):
        """Test that filtering works accurately."""
        # Test court filtering
        scotus_opinions = self.client.opinions.list(
            court="scotus",
            page_size=5
        )
        assert 'count' in scotus_opinions
        assert 'results' in scotus_opinions
        
        # Verify that all results are from SCOTUS
        for opinion in scotus_opinions['results']:
            if 'court' in opinion:
                assert 'scotus' in opinion['court'].lower()
    
    def test_date_filtering(self):
        """Test date filtering functionality."""
        # Test date range filtering
        recent_opinions = self.client.opinions.list(
            date_filed__gte="2023-01-01",
            page_size=5
        )
        assert 'count' in recent_opinions
        assert 'results' in recent_opinions
        
        # Verify that all results are from 2023 or later
        for opinion in recent_opinions['results']:
            if 'date_filed' in opinion:
                assert opinion['date_filed'].startswith('2023')
    
    def test_text_search_accuracy(self):
        """Test text search accuracy."""
        # Test specific term search
        search_results = self.client.search.list(
            q="Miranda rights",
            page_size=5
        )
        assert 'count' in search_results
        assert 'results' in search_results
        
        # Verify that results contain the search term
        for result in search_results['results']:
            if 'caseName' in result:
                assert 'miranda' in result['caseName'].lower() or 'rights' in result['caseName'].lower()
