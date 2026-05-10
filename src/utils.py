from datetime import datetime, timedelta
from dateutil import parser, tz

def parse_and_validate_window(start_str: str, end_str: str) -> tuple[datetime, datetime]:
    """
    Parses start and end datetime strings into local timezone-aware datetimes.
    Enforces PRD constraints: start < end, and duration <= 24 hours.
    """
    local_tz = tz.tzlocal()
    
    try:
        start_dt = parser.parse(start_str)
        end_dt = parser.parse(end_str)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid datetime format provided: {e}")

    # Enforce timezone awareness (defaulting to system local as per PRD)
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=local_tz)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=local_tz)

    if start_dt >= end_dt:
        raise ValueError(f"Validation Error: Start datetime ({start_dt}) must be strictly before end datetime ({end_dt}).")

    duration = end_dt - start_dt
    if duration > timedelta(hours=24):
        raise ValueError(f"Validation Error: Time window cannot exceed 24 hours. Requested window duration is {duration}.")

    return start_dt, end_dt

def format_duration(td: timedelta) -> str:
    """Formats a timedelta into a human-readable PRD-compliant string (e.g., '1h 30m')."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if hours > 0 and minutes > 0:
        return f"{hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{minutes}m"
