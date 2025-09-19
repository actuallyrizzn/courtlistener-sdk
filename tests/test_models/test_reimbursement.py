"""
Tests for Reimbursement model.
"""

import pytest
from courtlistener.models.reimbursement import Reimbursement


class TestReimbursement:
    """Test cases for Reimbursement model."""
    
    def test_reimbursement_creation(self):
        """Test creating a Reimbursement instance."""
        data = {
            "id": 1,
            "financial_disclosure": "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/",
            "judge": "https://api.courtlistener.com/api/rest/v4/judges/456/",
            "description": "Travel expenses for conference",
            "amount": 500.0,
            "date_created": "2023-01-01T00:00:00Z",
            "date_modified": "2023-01-02T00:00:00Z",
            "resource_uri": "https://api.courtlistener.com/api/rest/v4/reimbursements/1/",
            "absolute_url": "https://www.courtlistener.com/reimbursements/1/"
        }
        
        reimbursement = Reimbursement(data)
        
        assert reimbursement.id == 1
        assert reimbursement.financial_disclosure == "https://api.courtlistener.com/api/rest/v4/financial-disclosures/123/"
        assert reimbursement.judge == "https://api.courtlistener.com/api/rest/v4/judges/456/"
        assert reimbursement.description == "Travel expenses for conference"
        assert reimbursement.amount == 500.0
        assert reimbursement.date_created == "2023-01-01T00:00:00Z"
        assert reimbursement.date_modified == "2023-01-02T00:00:00Z"
        assert reimbursement.resource_uri == "https://api.courtlistener.com/api/rest/v4/reimbursements/1/"
        assert reimbursement.absolute_url == "https://www.courtlistener.com/reimbursements/1/"
    
    def test_reimbursement_with_none_values(self):
        """Test creating a Reimbursement with None values."""
        data = {
            "id": 1,
            "financial_disclosure": None,
            "judge": None,
            "description": None,
            "amount": None,
            "date_created": None,
            "date_modified": None,
            "resource_uri": None,
            "absolute_url": None
        }
        
        reimbursement = Reimbursement(data)
        
        assert reimbursement.id == 1
        assert reimbursement.financial_disclosure is None
        assert reimbursement.judge is None
        assert reimbursement.description is None
        assert reimbursement.amount is None
        assert reimbursement.date_created is None
        assert reimbursement.date_modified is None
        assert reimbursement.resource_uri is None
        assert reimbursement.absolute_url is None
