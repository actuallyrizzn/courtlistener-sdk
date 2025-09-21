"""
Integration tests for People and Organizations endpoints.
"""

import pytest
from unittest.mock import Mock, patch
from courtlistener import CourtListenerClient


class TestPeopleAndOrganizationsIntegration:
    """Integration tests for people and organizations endpoints."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = CourtListenerClient(api_token="test_token")
        # Mock the actual HTTP requests
        self.client._make_request = Mock()
        self.client.get = Mock()
        self.client.post = Mock()
        self.client.paginate = Mock()
    
    def test_people_workflow(self):
        """Test complete people workflow."""
        # Mock people list
        mock_people = {
            "count": 1,
            "results": [{
                "id": 1,
                "name": "John Smith",
                "position": "Judge",
                "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/"
            }]
        }
        self.client.get.return_value = mock_people
        
        # Test getting people
        people = self.client.people.list(name__icontains="Smith", position_type="Judge")
        assert people["count"] == 1
        assert len(people["results"]) == 1
        
        # Mock specific person
        mock_person = {
            "id": 1,
            "name": "John Smith",
            "position": "Judge",
            "court": "https://api.courtlistener.com/api/rest/v4/courts/scotus/",
            "education": "Harvard Law School"
        }
        self.client.get.return_value = mock_person
        
        # Test getting specific person
        person = self.client.people.get(1)
        assert person["id"] == 1
        assert person["name"] == "John Smith"
    
    def test_education_workflow(self):
        """Test education records workflow."""
        # Mock education records
        mock_educations = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "school": "https://api.courtlistener.com/api/rest/v4/schools/456/",
                    "degree": "J.D.",
                    "year": 1990
                },
                {
                    "id": 2,
                    "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                    "school": "https://api.courtlistener.com/api/rest/v4/schools/789/",
                    "degree": "B.A.",
                    "year": 1987
                }
            ]
        }
        self.client.get.return_value = mock_educations
        
        # Test getting education records
        educations = self.client.educations.list(person=123)
        assert educations["count"] == 2
        assert len(educations["results"]) == 2
        
        # Test getting specific education record
        mock_education = mock_educations["results"][0]
        self.client.get.return_value = mock_education
        
        education = self.client.educations.get(1)
        assert education["degree"] == "J.D."
        assert education["year"] == 1990
    
    def test_schools_workflow(self):
        """Test schools workflow."""
        # Mock schools list
        mock_schools = {
            "count": 1,
            "results": [{
                "id": 1,
                "name": "Harvard Law School",
                "type": "Law School",
                "location": "Cambridge, MA"
            }]
        }
        self.client.get.return_value = mock_schools
        
        # Test getting schools
        schools = self.client.schools.list()
        assert schools["count"] == 1
        assert len(schools["results"]) == 1
        
        # Test getting specific school
        mock_school = mock_schools["results"][0]
        self.client.get.return_value = mock_school
        
        school = self.client.schools.get(1)
        assert school["name"] == "Harvard Law School"
        assert school["type"] == "Law School"
    
    def test_aba_ratings_workflow(self):
        """Test ABA ratings workflow."""
        # Mock ABA ratings
        mock_ratings = {
            "count": 1,
            "results": [{
                "id": 1,
                "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                "rating": "Well Qualified",
                "year": 2020
            }]
        }
        self.client.get.return_value = mock_ratings
        
        # Test getting ABA ratings
        ratings = self.client.aba_ratings.list(person=123)
        assert ratings["count"] == 1
        assert len(ratings["results"]) == 1
        
        # Test getting specific rating
        mock_rating = mock_ratings["results"][0]
        self.client.get.return_value = mock_rating
        
        rating = self.client.aba_ratings.get(1)
        assert rating["rating"] == "Well Qualified"
        assert rating["year"] == 2020
    
    def test_political_affiliations_workflow(self):
        """Test political affiliations workflow."""
        # Mock political affiliations
        mock_affiliations = {
            "count": 1,
            "results": [{
                "id": 1,
                "person": "https://api.courtlistener.com/api/rest/v4/people/123/",
                "party": "Republican",
                "year": 2020
            }]
        }
        self.client.get.return_value = mock_affiliations
        
        # Test getting political affiliations
        affiliations = self.client.political_affiliations.list(person=123)
        assert affiliations["count"] == 1
        assert len(affiliations["results"]) == 1
        
        # Test getting specific affiliation
        mock_affiliation = mock_affiliations["results"][0]
        self.client.get.return_value = mock_affiliation
        
        affiliation = self.client.political_affiliations.get(1)
        assert affiliation["party"] == "Republican"
        assert affiliation["year"] == 2020
    
    def test_pagination_works_across_people_endpoints(self):
        """Test that pagination works across all people-related endpoints."""
        mock_iterator = Mock()
        self.client.paginate.return_value = mock_iterator
        
        people_endpoints = [
            'people',
            'schools',
            'educations',
            'aba_ratings',
            'political_affiliations'
        ]
        
        for endpoint_name in people_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.paginate()
            assert result == mock_iterator
    
    def test_get_methods_work_for_people_endpoints(self):
        """Test that get methods work for all people-related endpoints."""
        mock_response = {"id": 1, "name": "Test item"}
        self.client.get.return_value = mock_response
        
        people_endpoints = [
            'people',
            'schools',
            'educations',
            'aba_ratings',
            'political_affiliations'
        ]
        
        for endpoint_name in people_endpoints:
            endpoint = getattr(self.client, endpoint_name)
            result = endpoint.get(1)
            assert result == mock_response
