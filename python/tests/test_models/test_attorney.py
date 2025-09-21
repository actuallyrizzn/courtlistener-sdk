import pytest
from courtlistener.models.attorney import Attorney
from datetime import datetime


class TestAttorney:
    def test_from_dict_and_to_dict(self):
        """Test Attorney model serialization and deserialization."""
        data = {
            'id': 1,
            'name': 'John Smith',
            'firm': 'Smith & Associates',
            'contact': 'john.smith@lawfirm.com',
            'phone': '(555) 123-4567',
            'fax': '(555) 123-4568',
            'address1': '123 Main St',
            'address2': 'Suite 100',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20001',
            'absolute_url': '/attorney/1/',
            'resource_uri': '/api/rest/v4/attorneys/1/'
        }
        
        attorney = Attorney.from_dict(data)
        assert attorney.id == 1
        assert attorney.name == 'John Smith'
        assert attorney.firm == 'Smith & Associates'
        assert attorney.contact == 'john.smith@lawfirm.com'
        assert attorney.phone == '(555) 123-4567'
        assert attorney.fax == '(555) 123-4568'
        assert attorney.address1 == '123 Main St'
        assert attorney.address2 == 'Suite 100'
        assert attorney.city == 'Washington'
        assert attorney.state == 'DC'
        assert attorney.zip_code == '20001'
        assert attorney.absolute_url == '/attorney/1/'
        assert attorney.resource_uri == '/api/rest/v4/attorneys/1/'
        
        # Test to_dict
        d = attorney.to_dict()
        assert d['id'] == 1
        assert d['name'] == 'John Smith'
        assert d['firm'] == 'Smith & Associates'
        assert d['city'] == 'Washington'
    
    def test_edge_cases(self):
        """Test Attorney model edge cases."""
        # Missing optional fields
        attorney = Attorney.from_dict({'id': 2})
        assert attorney.id == 2
        assert attorney.name is None
        assert attorney.firm is None
        assert attorney.contact is None
        assert attorney.address1 is None
        
        # Empty strings
        attorney = Attorney.from_dict({
            'id': 3,
            'name': '',
            'firm': '',
            'address2': ''
        })
        assert attorney.name == ''
        assert attorney.firm == ''
        assert attorney.address2 == ''
    
    def test_properties(self):
        """Test Attorney model properties."""
        attorney = Attorney.from_dict({
            'id': 4,
            'address1': '123 Main St',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20001'
        })
        assert attorney.has_address is True
        
        attorney = Attorney.from_dict({'id': 5})
        assert attorney.has_address is False
        
        attorney = Attorney.from_dict({
            'id': 6,
            'phone': '(555) 123-4567'
        })
        assert attorney.has_phone is True
        
        attorney = Attorney.from_dict({'id': 7})
        assert attorney.has_phone is False
    
    def test_full_address(self):
        """Test Attorney full address property."""
        attorney = Attorney.from_dict({
            'id': 8,
            'address1': '123 Main St',
            'address2': 'Suite 100',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20001'
        })
        assert attorney.full_address == '123 Main St, Suite 100, Washington, DC 20001'
        
        attorney = Attorney.from_dict({
            'id': 9,
            'address1': '123 Main St',
            'city': 'Washington',
            'state': 'DC',
            'zip_code': '20001'
        })
        assert attorney.full_address == '123 Main St, Washington, DC 20001'
    
    def test_string_representations(self):
        """Test Attorney model string representations."""
        attorney = Attorney.from_dict({
            'id': 10,
            'name': 'John Smith',
            'firm': 'Smith & Associates'
        })
        
        assert str(attorney) == "Attorney(id=10, name='John Smith', firm='Smith & Associates')"
        assert repr(attorney) == "<Attorney(id=10, name='John Smith', firm='Smith & Associates', city=None)>" 