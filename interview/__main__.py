"""Main module to process weather event input from stdin."""
import json
import sys
from . import weather

def generate_input():
    """Capture and generate the input from STDIN."""
    for line in sys.stdin:
        yield json.loads(line)

for output in weather.process_events(generate_input()):
    print(json.dumps(output))
