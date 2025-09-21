"""
Comprehensive tests for Debt model.
"""

import pytest
from courtlistener.models.debt import Debt


class TestDebtComprehensive:
    def test_init_basic(self):
        """Test basic initialization."""
        data = {"id": 1, "description": "Test debt"}
        debt = Debt(data)
        assert debt._data == data

    def test_id_property(self):
        """Test id property."""
        data = {"id": 123}
        debt = Debt(data)
        assert debt.id == 123

    def test_id_property_none(self):
        """Test id property when None."""
        data = {}
        debt = Debt(data)
        assert debt.id is None

    def test_financial_disclosure_property(self):
        """Test financial_disclosure property."""
        data = {"financial_disclosure": "https://example.com/disclosure/123"}
        debt = Debt(data)
        assert debt.financial_disclosure == "https://example.com/disclosure/123"

    def test_financial_disclosure_property_none(self):
        """Test financial_disclosure property when None."""
        data = {}
        debt = Debt(data)
        assert debt.financial_disclosure is None

    def test_judge_property(self):
        """Test judge property."""
        data = {"judge": "https://example.com/judge/456"}
        debt = Debt(data)
        assert debt.judge == "https://example.com/judge/456"

    def test_judge_property_none(self):
        """Test judge property when None."""
        data = {}
        debt = Debt(data)
        assert debt.judge is None

    def test_description_property(self):
        """Test description property."""
        data = {"description": "Credit card debt"}
        debt = Debt(data)
        assert debt.description == "Credit card debt"

    def test_description_property_none(self):
        """Test description property when None."""
        data = {}
        debt = Debt(data)
        assert debt.description is None

    def test_amount_property(self):
        """Test amount property."""
        data = {"amount": 15000.50}
        debt = Debt(data)
        assert debt.amount == 15000.50

    def test_amount_property_none(self):
        """Test amount property when None."""
        data = {}
        debt = Debt(data)
        assert debt.amount is None

    def test_creditor_property(self):
        """Test creditor property."""
        data = {"creditor": "Bank of America"}
        debt = Debt(data)
        assert debt.creditor == "Bank of America"

    def test_creditor_property_none(self):
        """Test creditor property when None."""
        data = {}
        debt = Debt(data)
        assert debt.creditor is None

    def test_date_created_property(self):
        """Test date_created property."""
        data = {"date_created": "2023-01-01T12:00:00Z"}
        debt = Debt(data)
        assert hasattr(debt, 'date_created')

    def test_date_created_property_none(self):
        """Test date_created property when None."""
        data = {}
        debt = Debt(data)
        assert hasattr(debt, 'date_created')

    def test_date_modified_property(self):
        """Test date_modified property."""
        data = {"date_modified": "2023-01-15T10:30:00Z"}
        debt = Debt(data)
        assert hasattr(debt, 'date_modified')

    def test_date_modified_property_none(self):
        """Test date_modified property when None."""
        data = {}
        debt = Debt(data)
        assert hasattr(debt, 'date_modified')

    def test_resource_uri_property(self):
        """Test resource_uri property."""
        data = {"resource_uri": "/api/rest/v4/debts/123/"}
        debt = Debt(data)
        assert debt.resource_uri == "/api/rest/v4/debts/123/"

    def test_resource_uri_property_none(self):
        """Test resource_uri property when None."""
        data = {}
        debt = Debt(data)
        assert debt.resource_uri is None

    def test_absolute_url_property(self):
        """Test absolute_url property."""
        data = {"absolute_url": "https://www.courtlistener.com/debt/123/"}
        debt = Debt(data)
        assert debt.absolute_url == "https://www.courtlistener.com/debt/123/"

    def test_absolute_url_property_none(self):
        """Test absolute_url property when None."""
        data = {}
        debt = Debt(data)
        assert debt.absolute_url is None

    def test_comprehensive_data(self):
        """Test with comprehensive data."""
        data = {
            "id": 456,
            "financial_disclosure": "https://example.com/disclosure/456",
            "judge": "https://example.com/judge/789",
            "description": "Mortgage debt",
            "amount": 250000.00,
            "creditor": "Wells Fargo",
            "date_created": "2022-05-10T08:00:00Z",
            "date_modified": "2022-05-10T09:00:00Z",
            "absolute_url": "https://www.courtlistener.com/debt/456/",
            "resource_uri": "/api/rest/v4/debts/456/",
        }
        debt = Debt(data)
        assert debt.id == 456
        assert debt.financial_disclosure == "https://example.com/disclosure/456"
        assert debt.judge == "https://example.com/judge/789"
        assert debt.description == "Mortgage debt"
        assert debt.amount == 250000.00
        assert debt.creditor == "Wells Fargo"
        assert hasattr(debt, 'date_created')
        assert hasattr(debt, 'date_modified')
        assert debt.absolute_url == "https://www.courtlistener.com/debt/456/"
        assert debt.resource_uri == "/api/rest/v4/debts/456/"

    def test_edge_case_empty_data(self):
        """Test with completely empty data."""
        data = {}
        debt = Debt(data)
        
        # All properties should be None
        assert debt.id is None
        assert debt.financial_disclosure is None
        assert debt.judge is None
        assert debt.description is None
        assert debt.amount is None
        assert debt.creditor is None
        assert hasattr(debt, 'date_created')
        assert hasattr(debt, 'date_modified')
        assert debt.absolute_url is None
        assert debt.resource_uri is None

    def test_edge_case_partial_data(self):
        """Test with partial data."""
        data = {"id": 1, "description": "Test debt", "amount": 1000.0}
        debt = Debt(data)
        
        # Set properties should have values
        assert debt.id == 1
        assert debt.description == "Test debt"
        assert debt.amount == 1000.0
        
        # Unset properties should be None
        assert debt.financial_disclosure is None
        assert debt.judge is None
        assert debt.creditor is None
        assert hasattr(debt, 'date_created')
        assert hasattr(debt, 'date_modified')
        assert debt.absolute_url is None
        assert debt.resource_uri is None

    def test_edge_case_zero_amount(self):
        """Test with zero amount."""
        data = {"id": 1, "amount": 0.0, "description": "No debt"}
        debt = Debt(data)
        assert debt.amount == 0.0
        assert debt.description == "No debt"

    def test_edge_case_negative_amount(self):
        """Test with negative amount."""
        data = {"id": 1, "amount": -500.0, "description": "Credit balance"}
        debt = Debt(data)
        assert debt.amount == -500.0
        assert debt.description == "Credit balance"

    def test_edge_case_very_large_amount(self):
        """Test with very large amount."""
        data = {"id": 1, "amount": 999999999.99, "description": "Large debt"}
        debt = Debt(data)
        assert debt.amount == 999999999.99
        assert debt.description == "Large debt"

    def test_edge_case_empty_strings(self):
        """Test with empty string values."""
        data = {
            "id": 1,
            "description": "",
            "creditor": "",
            "financial_disclosure": "",
            "judge": ""
        }
        debt = Debt(data)
        assert debt.id == 1
        assert debt.description == ""
        assert debt.creditor == ""
        assert debt.financial_disclosure == ""
        assert debt.judge == ""
