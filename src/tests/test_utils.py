# src/tests/test_utils.py
import unittest
from datetime import timedelta
from src.utils import parse_and_validate_window, format_duration

class TestUtils(unittest.TestCase):
    def test_parse_and_validate_window_valid(self):
        start_str = "2026-05-07 09:00"
        end_str = "2026-05-07 18:00"
        start_dt, end_dt = parse_and_validate_window(start_str, end_str)
        
        self.assertIsNotNone(start_dt.tzinfo, "Start datetime must be timezone aware")
        self.assertIsNotNone(end_dt.tzinfo, "End datetime must be timezone aware")
        self.assertTrue(start_dt < end_dt)
        self.assertEqual((end_dt - start_dt).total_seconds(), 9 * 3600)

    def test_parse_and_validate_window_start_after_end(self):
        with self.assertRaisesRegex(ValueError, "strictly before"):
            parse_and_validate_window("2026-05-07 18:00", "2026-05-07 09:00")

    def test_parse_and_validate_window_exceeds_24h(self):
        with self.assertRaisesRegex(ValueError, "cannot exceed 24 hours"):
            parse_and_validate_window("2026-05-07 09:00", "2026-05-08 10:00")

    def test_format_duration(self):
        self.assertEqual(format_duration(timedelta(hours=1, minutes=30)), "1h 30m")
        self.assertEqual(format_duration(timedelta(hours=2)), "2h")
        self.assertEqual(format_duration(timedelta(minutes=45)), "45m")
        self.assertEqual(format_duration(timedelta(minutes=0)), "0m")

if __name__ == '__main__':
    unittest.main()
