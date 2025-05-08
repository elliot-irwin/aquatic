"""Unit tests for the weather module."""
from . import weather
import pytest

#ruff check . --select D

def test_process_events():
    """Test process_events function."""
    input_sample_data = {"type": "sample", "stationName": "Raleigh", "timestamp": 1672531300000, "temperature": 57.1}
    input_reset_control_data = {"type": "control", "command": "reset"}
    bad_data = {"type": "badtype", "stationName": "Raleigh", "timestamp": 1672531300000, "temperature": 57.1}
    
    #Test for Sample type
    assert [input_sample_data] == list(weather.process_events([input_sample_data]))

    #Test for control type
    reset_result = list(weather.process_events([input_reset_control_data]))
    assert reset_result[0]["type"] == "reset"

    
    #Ensure we get a ValueError when a bad type is passed in
    with pytest.raises(ValueError, match="Unknown Type encountered. Ignoring"):
        list(weather.process_events([bad_data]))


def test_store_data(monkeypatch):
    """Test store_data function."""
    testdata = dict({"type": "sample", "stationName": "Raleigh", "timestamp": 1672531300000, "temperature": 57.1})
    weather.store_data(testdata)
    assert "Raleigh" in weather.station_data


def test_get_timestamp(monkeypatch):
    """Test get_timestamp function."""
    ts_response = weather.get_timestamp()
    assert isinstance(ts_response, int)

def test_fetch_data(monkeypatch):
    """Test fetch_data function."""
    weather.station_data["Raleigh"] = {"high": 88, "low": 33}
    fetch_data_response = weather.fetch_data()
    assert fetch_data_response["type"] == "snapshot"
    assert "asOf" in fetch_data_response
    assert "Raleigh" in fetch_data_response["stations"]

def test_do_reset(monkeypatch):
    """Test do_reset function to ensure it has the required keys."""
    reset_response = weather.do_reset()
    assert reset_response["type"] == "reset"
