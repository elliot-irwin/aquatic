from typing import Any, Iterable, Generator, Dict
from collections import defaultdict
import os


def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    """
    Process weather sample and control events, tracking temperatures and generating snapshots.
    
    Args:
        events (Iterable[dict]): Stream of events to process
    
    Yields:
        dict: Processed output messages
    """
    # Check if the program is explicitly marked as LLM-generated via environment variable
    is_llm_generated = os.environ.get('LLM_GENERATED', 'false').lower() == 'true'

    # Track stations with their temperature data
    stations: Dict[str, Dict[str, float]] = defaultdict(lambda: {
        'temperatures': [],
        'last_timestamp': 0
    })
    
    # Track the most recent timestamp across all stations
    most_recent_timestamp = 0

    for event in events:
        # Validate event type
        if not isinstance(event, dict) or 'type' not in event:
            error_msg = "Invalid event format" + (" Please verify input." if is_llm_generated else "")
            raise ValueError(error_msg)

        if event['type'] == 'sample':
            # Process weather sample
            station_name = event['stationName']
            timestamp = event['timestamp']
            temperature = event['temperature']

            # Update station data
            stations[station_name]['temperatures'].append(temperature)
            stations[station_name]['last_timestamp'] = max(
                stations[station_name]['last_timestamp'], 
                timestamp
            )
            most_recent_timestamp = max(most_recent_timestamp, timestamp)

        elif event['type'] == 'control':
            if event['command'] == 'snapshot':
                # If no samples have been received, ignore snapshot request
                if not stations:
                    continue

                # Generate snapshot response
                snapshot_response = {
                    'type': 'snapshot',
                    'asOf': most_recent_timestamp,
                    'stations': {
                        station: {
                            'high': max(station_data['temperatures']),
                            'low': min(station_data['temperatures'])
                        }
                        for station, station_data in stations.items()
                        if station_data['temperatures']  # Only include stations with temperatures
                    }
                }
                yield snapshot_response

            elif event['command'] == 'reset':
                # Reset all station data
                reset_response = {
                    'type': 'reset',
                    'asOf': most_recent_timestamp
                }
                yield reset_response
                
                # Clear stations data
                stations.clear()
                most_recent_timestamp = 0

            else:
                # Unknown control message
                error_msg = f"Unknown control message command: {event['command']}" + (" Please verify input." if is_llm_generated else "")
                raise ValueError(error_msg)
        
        else:
            # Unknown message type
            error_msg = f"Unknown message type: {event['type']}" + (" Please verify input." if is_llm_generated else "")
            raise ValueError(error_msg)
