# src/calendar_service.py
import logging
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dateutil import parser
import dateutil.tz as tz

# Configure basic logging for the warning requirements
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_busy_intervals(creds: Credentials, calendar_ids: list[str], start_dt: datetime, end_dt: datetime) -> list[tuple[datetime, datetime]]:
    """
    Queries the Google Calendar Free/Busy API for the specified calendars.
    Ignores invalid calendars and returns a flat list of busy intervals (start, end).
    """
    if not calendar_ids:
        raise ValueError("Critical Error: The configuration file resulted in zero calendars to query.")

    # cache_discovery=False prevents an annoying warning about file cache in some local environments
    service = build('calendar', 'v3', credentials=creds, cache_discovery=False)

    # The Google API requires strict RFC3339 formatted strings
    time_min = start_dt.isoformat()
    time_max = end_dt.isoformat()

    # The freeBusy endpoint processes up to 50 calendars per request. 
    # For MVP, we assume the config contains < 50 items.
    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": cal_id} for cal_id in calendar_ids]
    }

    try:
        response = service.freebusy().query(body=body).execute()
    except Exception as e:
        raise RuntimeError(f"Failed to communicate with Google Calendar API: {e}")

    busy_intervals = []
    local_tz = tz.tzlocal()
    calendars_data = response.get('calendars', {})

    for cal_id, data in calendars_data.items():
        if 'errors' in data:
            logger.warning(f"Calendar '{cal_id}' is invalid or inaccessible. Skipping. Details: {data['errors']}")
            continue
        
        for busy_period in data.get('busy', []):
            # Parse Google's UTC/Offset strings back into local timezone-aware datetimes
            b_start = parser.isoparse(busy_period['start']).astimezone(local_tz)
            b_end = parser.isoparse(busy_period['end']).astimezone(local_tz)
            busy_intervals.append((b_start, b_end))

    return busy_intervals
