import argparse
import sys
import yaml
from pathlib import Path

from utils import parse_and_validate_window, format_duration
from auth import get_credentials, EnvironmentError
from calendar_service import get_busy_intervals
from processor import calculate_availability

def load_configuration() -> list[str]:
    """Loads target calendar IDs from the local config.yaml file."""
    config_path = Path(__file__).parent.parent / 'config.yaml'
    
    if not config_path.exists():
        print(f"Error: Configuration file not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        if not config or 'calendars' not in config:
            print("Error: Invalid config.yaml structure. Missing 'calendars' key.", file=sys.stderr)
            sys.exit(1)
            
        calendar_ids = config.get('calendars', [])
        # Extract ID if dictionary format was used in yaml, otherwise assume list of strings
        if all(isinstance(c, dict) for c in calendar_ids):
            return [c.get('id') for c in calendar_ids if c.get('id')]
        return [str(c) for c in calendar_ids if c]
        
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Calendar Availability Consolidator")
    parser.add_argument('--start', required=True, help="Start datetime (e.g., '2026-05-07 09:00')")
    parser.add_argument('--end', required=True, help="End datetime (e.g., '2026-05-07 18:00')")
    
    args = parser.parse_args()

    # Step 1: Input Validation
    try:
        start_dt, end_dt = parse_and_validate_window(args.start, args.end)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Step 2: Configuration & Auth
    calendar_ids = load_configuration()
    if not calendar_ids:
        print("Error: No valid calendars found in configuration.", file=sys.stderr)
        sys.exit(1)

    try:
        creds = get_credentials()
    except EnvironmentError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Step 3: Data Retrieval
    try:
        busy_intervals = get_busy_intervals(creds, calendar_ids, start_dt, end_dt)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # Step 4: Interval Processing
    results = calculate_availability(start_dt, end_dt, busy_intervals)

    # Step 5: Output Generation (PRD Format)
    print(f"\nTotal free time: {format_duration(results['total_available_time'])}\n")
    
    if not results['free_blocks']:
        print("No available blocks in this window.")
    else:
        print("Available blocks:")
        for block_start, block_end in results['free_blocks']:
            duration = block_end - block_start
            start_str = block_start.strftime("%H:%M")
            end_str = block_end.strftime("%H:%M")
            print(f"{start_str}-{end_str} ({format_duration(duration)})")

if __name__ == '__main__':
    main()
