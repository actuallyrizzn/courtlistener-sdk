"""
End-to-end tests for complete workflows across all endpoints.
"""

import pytest
import os
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestCompleteWorkflows:
    """End-to-end tests for complete workflows."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # These tests are designed to use mocks, so always create a test client
        # The CL_RUN_LIVE check should prevent these from running as live tests
        self.client = CourtListenerClient(api_token="test_token")
        # Mock all requests for testing using patch.object to properly replace methods
        self.client._make_request = Mock()
        # Use patch.object to properly mock bound methods
        self.get_patcher = patch.object(self.client, 'get', create=True)
        self.post_patcher = patch.object(self.client, 'post', create=True)
        self.paginate_patcher = patch.object(self.client, 'paginate', create=True)
        self.mock_get = self.get_patcher.start()
        self.mock_post = self.post_patcher.start()
        self.mock_paginate = self.paginate_patcher.start()
    
    def teardown_method(self):
        """Clean up test fixtures."""
        if self.get_patcher:
            self.get_patcher.stop()
        if self.post_patcher:
            self.post_patcher.stop()
        if self.paginate_patcher:
            self.paginate_patcher.stop()
    
    def test_legal_research_workflow(self):
        """Test complete legal research workflow."""
        # Step 1: Search for cases
        mock_search_results = {
            "count": 1,
            "results": [{
                "resource_uri": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                "caseName": "Test v. Test",
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
            }]
        }
        self.mock_get.return_value = mock_search_results
        
        search_results = self.client.search.list(q="constitutional law", court="scotus")
        assert search_results["count"] == 1
        
        # Step 2: Get specific opinion
        mock_opinion = {
            "id": 123,
            "caseName": "Test v. Test",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "date_filed": "2023-01-01"
        }
        self.mock_get.return_value = mock_opinion
        
        opinion = self.client.opinions.get(123)
        assert opinion["caseName"] == "Test v. Test"
        
        # Step 3: Get citations for the opinion
        mock_citations = {
            "count": 2,
            "results": [
                {
                    "citing_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/123/",
                    "cited_opinion": "https://api.courtlistener.com/api/rest/v4/opinions/456/"
                }
            ]
        }
        self.mock_get.return_value = mock_citations
        
        citations = self.client.opinions_cited.list(citing_opinion=123)
        assert citations["count"] == 2
        
        # Step 4: Get docket for the case
        mock_docket = {
            "id": 456,
            "case_name": "Test v. Test",
            "docket_number": "23-123"
        }
        self.mock_get.return_value = mock_docket
        
        docket = self.client.dockets.get(456)
        assert docket["case_name"] == "Test v. Test"
    
    def test_financial_disclosure_analysis_workflow(self):
        """Test complete financial disclosure analysis workflow."""
        # Step 1: Find a judge
        mock_judges = {
            "count": 1,
            "results": [{
                "id": 123,
                "name": "John Smith",
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
            }]
        }
        self.mock_get.return_value = mock_judges
        
        judges = self.client.judges.list(name__icontains="Smith")
        assert judges["count"] == 1
        
        # Step 2: Get financial disclosures for the judge
        mock_disclosures = {
            "count": 1,
            "results": [{
                "id": 1,
                "judge": "https://api.courtlistener.com/api/rest/v4/judges/123/",
                "year": 2023
            }]
        }
        self.mock_get.return_value = mock_disclosures
        
        disclosures = self.client.financial_disclosures.list(judge=123, year=2023)
        assert disclosures["count"] == 1
        
        # Step 3: Get investments
        mock_investments = {
            "count": 2,
            "results": [
                {"description": "Apple Stock", "value_min": 1000, "value_max": 5000},
                {"description": "Microsoft Stock", "value_min": 2000, "value_max": 6000}
            ]
        }
        self.mock_get.return_value = mock_investments
        
        investments = self.client.investments.list(financial_disclosure=1)
        assert investments["count"] == 2
        
        # Step 4: Get gifts
        mock_gifts = {
            "count": 1,
            "results": [{"description": "Conference attendance", "value": 2500}]
        }
        self.mock_get.return_value = mock_gifts
        
        gifts = self.client.gifts.list(financial_disclosure=1)
        assert gifts["count"] == 1
    
    def test_alert_management_workflow(self):
        """Test complete alert management workflow."""
        # Step 1: Create a search alert
        mock_created_alert = {
            "id": 1,
            "name": "Constitutional Law Alert",
            "query": "constitutional",
            "rate": "wly",
            "alert_type": "search"
        }
        self.mock_post.return_value = mock_created_alert
        
        alert = self.client.alerts.create(
            name="Constitutional Law Alert",
            query="constitutional",
            rate="wly",
            alert_type="search"
        )
        assert alert["id"] == 1
        
        # Step 2: List all alerts
        mock_alerts = {
            "count": 1,
            "results": [mock_created_alert]
        }
        self.mock_get.return_value = mock_alerts
        
        alerts = self.client.alerts.list()
        assert alerts["count"] == 1
        
        # Step 3: Update the alert
        mock_updated_alert = {
            "id": 1,
            "name": "Constitutional Law Alert",
            "query": "constitutional",
            "rate": "dly",
            "alert_type": "search"
        }
        self.mock_post.return_value = mock_updated_alert
        
        updated_alert = self.client.alerts.update(1, rate="dly")
        assert updated_alert["rate"] == "dly"
        
        # Step 4: Create a docket alert
        mock_docket_alert = {
            "id": 2,
            "docket": "https://api.courtlistener.com/api/rest/v4/dockets/456/",
            "alert_type": "entry"
        }
        self.mock_post.return_value = mock_docket_alert
        
        docket_alert = self.client.docket_alerts.create(docket=456, alert_type="entry")
        assert docket_alert["id"] == 2
        
        # Step 5: Delete alerts
        self.client.alerts.delete(1)
        self.client.docket_alerts.delete(2)
    
    def test_people_and_education_workflow(self):
        """Test complete people and education workflow."""
        # Step 1: Search for people
        mock_people = {
            "count": 1,
            "results": [{
                "id": 123,
                "name": "John Smith",
                "position": "Judge",
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
            }]
        }
        self.mock_get.return_value = mock_people
        
        people = self.client.people.list(name__icontains="Smith", position_type="Judge")
        assert people["count"] == 1
        
        # Step 2: Get education records
        mock_educations = {
            "count": 2,
            "results": [
                {
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "school": "https://api.courtlistener.com/api/rest/v4/schools/456/",
                    "degree": "J.D.",
                    "year": 1990
                }
            ]
        }
        self.mock_get.return_value = mock_educations
        
        educations = self.client.educations.list(person=123)
        assert educations["count"] == 2
        
        # Step 3: Get school information
        mock_school = {
            "id": 456,
            "name": "Harvard Law School",
            "type": "Law School",
            "location": "Cambridge, MA"
        }
        self.mock_get.return_value = mock_school
        
        school = self.client.schools.get(456)
        assert school["name"] == "Harvard Law School"
        
        # Step 4: Get ABA ratings
        mock_ratings = {
            "count": 1,
            "results": [{
                "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                "rating": "Well Qualified",
                "year": 2020
            }]
        }
        self.mock_get.return_value = mock_ratings
        
        ratings = self.client.aba_ratings.list(person=123)
        assert ratings["count"] == 1
    
    def test_recap_document_workflow(self):
        """Test complete RECAP document workflow."""
        # Step 1: Get dockets
        mock_dockets = {
            "count": 1,
            "results": [{
                "id": 456,
                "case_name": "Test v. Test",
                "docket_number": "23-123"
            }]
        }
        self.mock_get.return_value = mock_dockets
        
        dockets = self.client.dockets.list(court="scotus")
        assert dockets["count"] == 1
        
        # Step 2: Get docket entries
        mock_entries = {
            "count": 1,
            "results": [{
                "id": 789,
                "docket": "https://api.courtlistener.com/api/rest/v4/dockets/456/",
                "entry_number": 1
            }]
        }
        self.mock_get.return_value = mock_entries
        
        entries = self.client.docket_entries.list(docket=456)
        assert entries["count"] == 1
        
        # Step 3: Get RECAP documents
        mock_documents = {
            "count": 1,
            "results": [{
                "id": 101,
                "docket_entry": "https://api.courtlistener.com/api/rest/v4/docket-entries/789/",
                "file_url": "https://example.com/document.pdf",
                "file_type": "pdf"
            }]
        }
        self.mock_get.return_value = mock_documents
        
        documents = self.client.recap_documents.list(docket_entry=789)
        assert documents["count"] == 1
        
        # Step 4: Get parties
        mock_parties = {
            "count": 2,
            "results": [
                {"name": "Plaintiff", "type": "Plaintiff"},
                {"name": "Defendant", "type": "Defendant"}
            ]
        }
        self.mock_get.return_value = mock_parties
        
        parties = self.client.parties.list(docket=456)
        assert parties["count"] == 2
