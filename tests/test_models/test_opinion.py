import pytest
from courtlistener.models.opinion import Opinion
from datetime import datetime


class TestOpinion:
    def test_from_dict_and_to_dict(self):
        """Test Opinion model serialization and deserialization."""
        data = {
            'id': 1,
            'cluster': 1,
            'author': 1,
            'joined_by': [2, 3],
            'type': '010combined',
            'type_name': 'Majority Opinion',
            'html': '<p>This is the opinion text</p>',
            'html_lawbox': '<p>Lawbox version</p>',
            'html_columbia': '<p>Columbia version</p>',
            'html_anon_2020': '<p>Anonymous version</p>',
            'plain_text': 'This is the opinion text',
            'html_with_citations': '<p>Opinion with citations</p>',
            'absolute_url': '/opinion/1/',
            'resource_uri': '/api/rest/v4/opinions/1/'
        }
        
        opinion = Opinion.from_dict(data)
        assert opinion.id == 1
        assert opinion.cluster == 1
        assert opinion.author == 1
        assert opinion.joined_by == [2, 3]
        assert opinion.type == '010combined'
        assert opinion.type_name == 'Majority Opinion'
        assert opinion.html == '<p>This is the opinion text</p>'
        assert opinion.html_lawbox == '<p>Lawbox version</p>'
        assert opinion.html_columbia == '<p>Columbia version</p>'
        assert opinion.html_anon_2020 == '<p>Anonymous version</p>'
        assert opinion.plain_text == 'This is the opinion text'
        assert opinion.html_with_citations == '<p>Opinion with citations</p>'
        assert opinion.absolute_url == '/opinion/1/'
        assert opinion.resource_uri == '/api/rest/v4/opinions/1/'
        
        # Test to_dict
        d = opinion.to_dict()
        assert d['id'] == 1
        assert d['cluster'] == 1
        assert d['author'] == 1
        assert d['joined_by'] == [2, 3]
        assert d['type'] == '010combined'
    
    def test_edge_cases(self):
        """Test Opinion model edge cases."""
        # Missing optional fields
        opinion = Opinion.from_dict({'id': 2})
        assert opinion.id == 2
        assert opinion.cluster is None
        assert opinion.author is None
        assert opinion.joined_by == []
        assert opinion.type is None
        assert opinion.html is None
        
        # Empty joined_by
        opinion = Opinion.from_dict({'id': 3, 'joined_by': None})
        assert opinion.joined_by is None
    
    def test_properties(self):
        """Test Opinion model properties."""
        opinion = Opinion.from_dict({
            'id': 4,
            'type': '010combined'
        })
        assert opinion.is_majority_opinion is True
        
        opinion = Opinion.from_dict({
            'id': 5,
            'type': '020concurring'
        })
        assert opinion.is_concurring_opinion is True
        
        opinion = Opinion.from_dict({
            'id': 6,
            'type': '030dissenting'
        })
        assert opinion.is_dissenting_opinion is True
        
        opinion = Opinion.from_dict({
            'id': 7,
            'type': 'unknown'
        })
        assert opinion.is_majority_opinion is False
        assert opinion.is_concurring_opinion is False
        assert opinion.is_dissenting_opinion is False
    
    def test_string_representations(self):
        """Test Opinion model string representations."""
        opinion = Opinion.from_dict({
            'id': 8,
            'type': '010combined',
            'type_name': 'Majority Opinion'
        })
        
        assert str(opinion) == "Opinion(id=8, type='010combined', type_name='Majority Opinion')"
        assert repr(opinion) == "<Opinion(id=8, cluster=None, author=None, type='010combined')>" 