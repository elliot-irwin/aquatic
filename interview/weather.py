"""Module to handle weather data processing and state management."""
from typing import Any, Iterable, Generator
import time

#RavzPC@RUDE-2021 /cygdrive/z/Repositories/streaming_interview
#clear; cat input.txt | python -m interview

station_data = dict()

def store_data(line):
    """Store the input data in a dictionary station_data."""
    input_station = line["stationName"]

    input_temperature = line["temperature"]
    if input_station not in station_data:
        station_data[input_station] = {
            "high": input_temperature,
            "low": input_temperature
        }
    else:
        curr_high = station_data[input_station]["high"]
        curr_low = station_data[input_station]["low"]
        station_data[input_station]["high"] = max(curr_high, input_temperature)
        station_data[input_station]["low"] = min(curr_low, input_temperature)



def get_timestamp():
    """Generate the timestamp."""
    return int(time.time() * 1000)

def fetch_data():
    """Fetch data in station_data and return it."""
    current_timestamp = get_timestamp()

    snapshot_response = dict({"type": "snapshot", 
                              "asOf": current_timestamp,
                              "stations": station_data})
    return(snapshot_response)

def do_reset():
    """Reset and clear out data in station_data."""
    station_data.clear()
    current_timestamp = get_timestamp()
    reset_response = dict({"type": "reset", "asOf": current_timestamp})
    return(reset_response)

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    """Process the input events and yield output records."""
    for line in events:
        line_type = line['type']
        if line_type=='sample':
            store_data(line)
            yield line
        elif line_type=="control":
            line_command = line["command"]
            if line_command=="reset":
                yield(do_reset())
            elif line_command=="snapshot":
                yield(fetch_data())
        else:
            raise ValueError("Unknown Type encountered. Ignoring")
        
