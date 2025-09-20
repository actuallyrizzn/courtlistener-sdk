import pytest
from courtlistener.models.financial import (
    FinancialDisclosure, Investment, NonInvestmentIncome, Agreement, Gift, Reimbursement, Debt, Financial
)
from datetime import datetime


class TestFinancialDisclosure:
    def test_from_dict_and_to_dict(self):
        data = {
            'id': 1,
            'date_received': '2020-01-01T00:00:00Z',
            'description': 'Disclosure',
        }
        obj = FinancialDisclosure.from_dict(data)
        assert obj.id == 1
        assert hasattr(obj, 'date_received')
        assert obj.description == 'Disclosure'
        d = obj.to_dict()
        assert d['id'] == 1
        assert d['description'] == 'Disclosure'


class TestInvestment:
    def test_from_dict_and_to_dict(self):
        data = {'id': 2, 'description': 'Investment'}
        obj = Investment.from_dict(data)
        assert obj.id == 2
        assert obj.description == 'Investment'
        d = obj.to_dict()
        assert d['id'] == 2
        assert d['description'] == 'Investment'


class TestNonInvestmentIncome:
    def test_from_dict_and_to_dict(self):
        data = {'id': 3, 'description': 'Non-Investment Income'}
        obj = NonInvestmentIncome.from_dict(data)
        assert obj.id == 3
        assert obj.description == 'Non-Investment Income'
        d = obj.to_dict()
        assert d['id'] == 3
        assert d['description'] == 'Non-Investment Income'


class TestAgreement:
    def test_from_dict_and_to_dict(self):
        data = {'id': 4, 'description': 'Agreement'}
        obj = Agreement.from_dict(data)
        assert obj.id == 4
        assert obj.description == 'Agreement'
        d = obj.to_dict()
        assert d['id'] == 4
        assert d['description'] == 'Agreement'


class TestGift:
    def test_from_dict_and_to_dict(self):
        data = {'id': 5, 'description': 'Gift'}
        obj = Gift.from_dict(data)
        assert obj.id == 5
        assert obj.description == 'Gift'
        d = obj.to_dict()
        assert d['id'] == 5
        assert d['description'] == 'Gift'


class TestReimbursement:
    def test_from_dict_and_to_dict(self):
        data = {'id': 6, 'description': 'Reimbursement'}
        obj = Reimbursement.from_dict(data)
        assert obj.id == 6
        assert obj.description == 'Reimbursement'
        d = obj.to_dict()
        assert d['id'] == 6
        assert d['description'] == 'Reimbursement'


class TestDebt:
    def test_from_dict_and_to_dict(self):
        data = {'id': 7, 'description': 'Debt'}
        obj = Debt.from_dict(data)
        assert obj.id == 7
        assert obj.description == 'Debt'
        d = obj.to_dict()
        assert d['id'] == 7
        assert d['description'] == 'Debt'


class TestFinancial:
    def test_from_dict_and_to_dict(self):
        """Test Financial model serialization and deserialization."""
        data = {
            'id': 1,
            'docket': 1,
            'type': 'filing_fee',
            'amount': 350.00,
            'date': '2020-01-01T00:00:00Z',
            'description': 'Filing fee for civil case',
            'absolute_url': '/financial/1/',
            'resource_uri': '/api/rest/v4/financial/1/'
        }
        
        financial = Financial.from_dict(data)
        assert financial.id == 1
        assert financial.docket == 1
        assert financial.type == 'filing_fee'
        assert financial.amount == 350.00
        assert hasattr(financial, 'date')
        assert financial.description == 'Filing fee for civil case'
        assert financial.absolute_url == '/financial/1/'
        assert financial.resource_uri == '/api/rest/v4/financial/1/'
        
        # Test to_dict
        d = financial.to_dict()
        assert d['id'] == 1
        assert d['docket'] == 1
        assert d['type'] == 'filing_fee'
        assert d['amount'] == 350.00
    
    def test_edge_cases(self):
        """Test Financial model edge cases."""
        # Missing optional fields
        financial = Financial.from_dict({'id': 2})
        assert financial.id == 2
        assert financial.docket is None
        assert financial.type is None
        assert financial.amount is None
        assert financial.date is None
        assert financial.description is None
        
        # Zero amount
        financial = Financial.from_dict({
            'id': 3,
            'amount': 0.00
        })
        assert financial.amount == 0.00
        
        # Invalid dates
        financial = Financial.from_dict({'id': 4, 'date': 'not-a-date'})
        assert financial.date is None
    
    def test_properties(self):
        """Test Financial model properties."""
        financial = Financial.from_dict({
            'id': 5,
            'type': 'filing_fee'
        })
        assert financial.is_filing_fee is True
        
        financial = Financial.from_dict({
            'id': 6,
            'type': 'costs'
        })
        assert financial.is_costs is True
        
        financial = Financial.from_dict({
            'id': 7,
            'type': 'damages'
        })
        assert financial.is_damages is True
        
        financial = Financial.from_dict({
            'id': 8,
            'type': 'unknown'
        })
        assert financial.is_filing_fee is False
        assert financial.is_costs is False
        assert financial.is_damages is False
        
        financial = Financial.from_dict({
            'id': 9,
            'amount': 100.00
        })
        assert financial.is_positive is True
        
        financial = Financial.from_dict({
            'id': 10,
            'amount': -50.00
        })
        assert financial.is_negative is True
    
    def test_amount_formatted(self):
        """Test Financial amount formatting."""
        financial = Financial.from_dict({
            'id': 11,
            'amount': 1234.56
        })
        assert financial.amount_formatted == '$1,234.56'
        
        financial = Financial.from_dict({
            'id': 12,
            'amount': -567.89
        })
        assert financial.amount_formatted == '-$567.89'
        
        financial = Financial.from_dict({
            'id': 13,
            'amount': 0.00
        })
        assert financial.amount_formatted == '$0.00'
        
        financial = Financial.from_dict({'id': 14})
        assert financial.amount_formatted == '$0.00'
    
    def test_string_representations(self):
        """Test Financial model string representations."""
        financial = Financial.from_dict({
            'id': 15,
            'type': 'filing_fee',
            'amount': 350.00
        })
        
        assert str(financial) == "<Financial(id=15, docket=None, type='filing_fee', amount=350.0)>"
        assert repr(financial) == "<Financial(id=15, docket=None, type='filing_fee', amount=350.0)>" 