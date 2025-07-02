from typing import Any, Iterable, Generator, Dict
from collections import defaultdict

class WeatherStation:
    def __init__(self) -> None:
        self.high: float = float('-inf')
        self.low: float = float('inf')
    
    def update(self, temperature: float) -> None:
        self.high = max(self.high, temperature)
        self.low = min(self.low, temperature)

def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    stations: Dict[str, WeatherStation] = defaultdict(WeatherStation)
    latest_timestamp: int = 0
    
    for event in events:
        event_type = event.get('type')
        
        if event_type == 'sample':
            station_name = event['stationName']
            temperature = event['temperature']
            timestamp = event['timestamp']
            
            latest_timestamp = max(latest_timestamp, timestamp)
            stations[station_name].update(temperature)
            
        elif event_type == 'control':
            command = event.get('command')
            
            if command == 'snapshot' and latest_timestamp > 0:
                yield {
                    'type': 'snapshot',
                    'asOf': latest_timestamp,
                    'stations': {
                        name: {'high': station.high, 'low': station.low}
                        for name, station in stations.items()
                        if station.high != float('-inf')
                    }
                }
            elif command == 'reset':
                if latest_timestamp > 0:
                    yield {
                        'type': 'reset',
                        'asOf': latest_timestamp
                    }
                stations.clear()
                latest_timestamp = 0
            else:
                raise ValueError("Unknown command. Please verify input.")
                
        else:
            raise ValueError("Unknown message type. Please verify input.")
