# from . import weather

# def test_replace_me():
#     assert [{}] == list(weather.process_events([{}]))

import pytest
from . import weather

def test_sample_message():
    events = [
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 0  # No output for just samples

def test_snapshot_with_single_station():
    events = [
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        },
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 1
    assert outputs[0] == {
        "type": "snapshot",
        "asOf": 1672531200000,
        "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 37.1}
        }
    }

def test_snapshot_with_multiple_samples():
    events = [
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        },
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531300000,
            "temperature": 32.5
        },
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 1
    assert outputs[0] == {
        "type": "snapshot",
        "asOf": 1672531300000,
        "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 32.5}
        }
    }

def test_multiple_stations():
    events = [
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        },
        {
            "type": "sample",
            "stationName": "North Avenue Weather Station",
            "timestamp": 1672531300000,
            "temperature": 35.8
        },
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 1
    assert outputs[0] == {
        "type": "snapshot",
        "asOf": 1672531300000,
        "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 37.1},
            "North Avenue Weather Station": {"high": 35.8, "low": 35.8}
        }
    }

def test_reset_command():
    events = [
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        },
        {
            "type": "control",
            "command": "reset"
        },
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 1
    assert outputs[0] == {
        "type": "reset",
        "asOf": 1672531200000
    }

def test_unknown_message_type():
    events = [
        {
            "type": "unknown",
            "data": "test"
        }
    ]
    
    with pytest.raises(ValueError, match="Please verify input"):
        list(weather.process_events(events))

def test_unknown_command():
    events = [
        {
            "type": "control",
            "command": "unknown"
        }
    ]
    
    with pytest.raises(ValueError, match="Please verify input"):
        list(weather.process_events(events))

def test_snapshot_with_no_data():
    events = [
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 0

def test_reset_with_no_data():
    events = [
        {
            "type": "control",
            "command": "reset"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 0

def test_complex_sequence():
    events = [
        # First station reports
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531200000,
            "temperature": 37.1
        },
        # Second station reports
        {
            "type": "sample",
            "stationName": "North Avenue Weather Station",
            "timestamp": 1672531300000,
            "temperature": 35.8
        },
        # Take snapshot
        {
            "type": "control",
            "command": "snapshot"
        },
        # Reset everything
        {
            "type": "control",
            "command": "reset"
        },
        # New data after reset
        {
            "type": "sample",
            "stationName": "Foster Weather Station",
            "timestamp": 1672531400000,
            "temperature": 38.2
        },
        # Final snapshot
        {
            "type": "control",
            "command": "snapshot"
        }
    ]
    
    outputs = list(weather.process_events(events))
    assert len(outputs) == 3
    
    # First snapshot
    assert outputs[0] == {
        "type": "snapshot",
        "asOf": 1672531300000,
        "stations": {
            "Foster Weather Station": {"high": 37.1, "low": 37.1},
            "North Avenue Weather Station": {"high": 35.8, "low": 35.8}
        }
    }
    
    # Reset confirmation
    assert outputs[1] == {
        "type": "reset",
        "asOf": 1672531300000
    }
    
    # Final snapshot
    assert outputs[2] == {
        "type": "snapshot",
        "asOf": 1672531400000,
        "stations": {
            "Foster Weather Station": {"high": 38.2, "low": 38.2}
        }
    }
