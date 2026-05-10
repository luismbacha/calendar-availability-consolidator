# src/tests/test_calendar_service.py
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from dateutil import tz
from src.calendar_service import get_busy_intervals
from google.oauth2.credentials import Credentials

class TestCalendarService(unittest.TestCase):

    def setUp(self):
        self.local_tz = tz.tzlocal()
        self.start_dt = datetime(2026, 5, 7, 9, 0, tzinfo=self.local_tz)
        self.end_dt = datetime(2026, 5, 7, 18, 0, tzinfo=self.local_tz)
        self.mock_creds = MagicMock(spec=Credentials)

    @patch('src.calendar_service.build')
    def test_get_busy_intervals_success(self, mock_build):
        # Mocking the Google API response structure
        mock_service = MagicMock()
        mock_query = MagicMock()
        mock_execute = MagicMock()
        
        mock_build.return_value = mock_service
        mock_service.freebusy.return_value = mock_query
        mock_query.query.return_value = mock_execute
        
        mock_execute.return_value = {
            "calendars": {
                "primary": {
                    "busy": [
                        {"start": "2026-05-07T10:00:00Z", "end": "2026-05-07T11:00:00Z"}
                    ]
                },
                "invalid@calendar.com": {
                    "errors": [{"reason": "notFound"}]
                }
            }
        }

        calendars = ["primary", "invalid@calendar.com"]
        intervals = get_busy_intervals(self.mock_creds, calendars, self.start_dt, self.end_dt)

        self.assertEqual(len(intervals), 1)
        # Check if the returned interval is properly converted to a datetime object
        self.assertEqual(intervals[0][0].year, 2026)
        self.assertEqual(intervals[0][0].month, 5)

    def test_get_busy_intervals_empty_list(self):
        with self.assertRaisesRegex(ValueError, "zero calendars to query"):
            get_busy_intervals(self.mock_creds, [], self.start_dt, self.end_dt)

if __name__ == '__main__':
    unittest.main()
