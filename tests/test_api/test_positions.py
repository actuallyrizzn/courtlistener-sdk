import pytest
from unittest.mock import MagicMock
from courtlistener.api.positions import PositionsAPI
from courtlistener.models.position import Position

def make_api():
    mock_client = MagicMock()
    api = PositionsAPI(mock_client)
    return api, mock_client

def test_list_positions():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 1}]}
    results = api.list_positions()
    assert isinstance(results[0], Position)
    assert results[0].id == 1
    mock_client.get.assert_called_once()

def test_get_position():
    api, mock_client = make_api()
    mock_client.get.return_value = {'id': 2}
    pos = api.get_position(2)
    assert isinstance(pos, Position)
    assert pos.id == 2
    mock_client.get.assert_called_once()

def test_get_positions_by_judge():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 3}]}
    results = api.get_positions_by_judge(5)
    assert results[0].id == 3
    mock_client.get.assert_called_once()

def test_get_positions_by_court():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 4}]}
    results = api.get_positions_by_court(7)
    assert results[0].id == 4
    mock_client.get.assert_called_once()

def test_get_active_positions():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 5}]}
    results = api.get_active_positions()
    assert results[0].id == 5
    mock_client.get.assert_called_once()

def test_get_positions_by_position_type():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 6}]}
    results = api.get_positions_by_position_type('jud')
    assert results[0].id == 6
    mock_client.get.assert_called_once()

def test_get_positions_by_date_range():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 7}]}
    results = api.get_positions_by_date_range('2020-01-01', '2020-12-31')
    assert results[0].id == 7
    mock_client.get.assert_called_once()

def test_get_positions_by_nomination_process():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 8}]}
    results = api.get_positions_by_nomination_process('Presidential')
    assert results[0].id == 8
    mock_client.get.assert_called_once()

def test_get_positions_by_supervisor():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 9}]}
    results = api.get_positions_by_supervisor(12)
    assert results[0].id == 9
    mock_client.get.assert_called_once()

def test_get_positions_by_jurisdiction():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 10}]}
    results = api.get_positions_by_jurisdiction('F')
    assert results[0].id == 10
    mock_client.get.assert_called_once()

def test_get_current_position_for_judge():
    api, mock_client = make_api()
    mock_client.get.return_value = {'results': [{'id': 11}]}
    pos = api.get_current_position_for_judge(15)
    assert pos.id == 11
    mock_client.get.assert_called_once() 