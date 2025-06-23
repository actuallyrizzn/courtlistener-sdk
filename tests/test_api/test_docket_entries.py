import pytest
from unittest.mock import MagicMock
from courtlistener.api.docket_entries import DocketEntriesAPI
from courtlistener.models.docket_entry import DocketEntry

def make_api():
    mock_client = MagicMock()
    api = DocketEntriesAPI(mock_client)
    return api, mock_client

def test_list_entries():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 1}, {'id': 2}]}
    results = api.list_entries(docket_id=42)
    assert isinstance(results[0], DocketEntry)
    assert results[0].id == 1
    mock_client.get.assert_called_once()

def test_get_entry():
    api, mock_client = make_api()
    mock_client.get.return_value = {'id': 5}
    entry = api.get_entry(5)
    assert isinstance(entry, DocketEntry)
    assert entry.id == 5
    mock_client.get.assert_called_once()

def test_get_entries_by_date_range():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 3}]}
    results = api.get_entries_by_date_range(42, '2020-01-01', '2020-12-31')
    assert results[0].id == 3
    mock_client.get.assert_called_once()

def test_get_entries_by_number():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 4}]}
    results = api.get_entries_by_number(42, 7)
    assert results[0].id == 4
    mock_client.get.assert_called_once()

def test_get_entries_by_description():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 6}]}
    results = api.get_entries_by_description(42, 'order')
    assert results[0].id == 6
    mock_client.get.assert_called_once()

def test_get_entries_with_documents():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 8}]}
    results = api.get_entries_with_documents(42)
    assert results[0].id == 8
    mock_client.get.assert_called_once() 