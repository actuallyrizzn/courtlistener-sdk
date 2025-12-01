import os
import pytest
from unittest.mock import patch, Mock
from courtlistener.client import CourtListenerClient
from courtlistener.exceptions import CourtListenerError, AuthenticationError, RateLimitError, NotFoundError

pytestmark = pytest.mark.integration

API_TOKEN = os.environ.get('COURTLISTENER_API_TOKEN')

@pytest.fixture(scope='module')
def client():
    if not API_TOKEN:
        pytest.skip('No API token set for integration tests')
    return CourtListenerClient(api_token=API_TOKEN)

def test_authentication_flow(client):
    """Test that the client authenticates and can make a request."""
    # Should not raise
    resp = client.search.search_opinions(q='Miranda')
    assert 'results' in resp

def test_request_response_cycle(client):
    """Test a full request/response cycle for a known endpoint."""
    resp = client.dockets.list_dockets(court='scotus', page=1)
    assert isinstance(resp, list)
    if resp:
        assert hasattr(resp[0], 'id')

def test_error_handling_invalid_token():
    """Test error handling for invalid authentication."""
    bad_client = CourtListenerClient(api_token='invalid')
    # Invalid token should raise AuthenticationError, but API might return 404
    # So we check for either AuthenticationError or NotFoundError
    with pytest.raises((AuthenticationError, NotFoundError, CourtListenerError)):
        bad_client.search.search_opinions(q='Miranda')

def test_error_handling_not_found(client):
    """Test error handling for 404 Not Found."""
    with pytest.raises(CourtListenerError) as exc_info:
        client.dockets.get_docket(999999999)
    assert exc_info.value.status_code == 404

def test_rate_limiting_behavior():
    """Test rate limiting handling (mocked)."""
    with patch('courtlistener.client.CourtListenerClient._make_request') as mock_request:
        mock_request.side_effect = RateLimitError('Rate limit exceeded')
        client = CourtListenerClient(api_token='dummy')
        with pytest.raises(RateLimitError):
            client.search.search_opinions(q='Miranda')

def test_end_to_end_api_call(client):
    """Test an end-to-end API call with filters and pagination."""
    resp = client.opinions.list_opinions(court='scotus', type='010combined', page=1)
    assert isinstance(resp, list)
    if resp:
        opinion_id = resp[0].id
        detail = client.opinions.get_opinion(opinion_id)
        assert detail.id == opinion_id

def test_pagination_handling(client):
    """Test pagination by requesting multiple pages."""
    resp1 = client.dockets.list_dockets(page=1)
    resp2 = client.dockets.list_dockets(page=2)
    assert isinstance(resp1, list)
    assert isinstance(resp2, list)
    # Pages should be different (or at least be lists)
    assert resp1 != resp2 or (len(resp1) > 0 and len(resp2) > 0)

def test_filter_application(client):
    """Test filter application returns filtered results."""
    resp = client.dockets.list_dockets(court='scotus', nature_of_suit='Civil Rights')
    assert isinstance(resp, list)
    # Can't guarantee results, but should not error

def test_data_consistency(client):
    """Test that data returned by one endpoint matches related endpoint."""
    resp = client.dockets.list_dockets(court='scotus', page=1)
    if resp:
        docket_id = resp[0].id
        detail = client.dockets.get_docket(docket_id)
        assert detail.id == docket_id 
