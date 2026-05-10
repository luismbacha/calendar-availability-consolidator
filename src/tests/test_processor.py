import unittest
from datetime import datetime, timedelta
from src.processor import merge_intervals, calculate_availability

class TestProcessor(unittest.TestCase):

    def setUp(self):
        # Base arbitrary date for testing logic
        self.base = datetime(2026, 5, 7, 9, 0)
        self.window_end = self.base + timedelta(hours=9) # 18:00

    def test_merge_intervals_overlapping_and_adjacent(self):
        intervals = [
            (self.base, self.base + timedelta(hours=1)),                     # 09:00 - 10:00
            (self.base + timedelta(minutes=30), self.base + timedelta(hours=2)), # 09:30 - 11:00 (overlaps)
            (self.base + timedelta(hours=2), self.base + timedelta(hours=3))     # 11:00 - 12:00 (adjacent)
        ]
        merged = merge_intervals(intervals)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0][0], self.base)
        self.assertEqual(merged[0][1], self.base + timedelta(hours=3))

    def test_calculate_availability_with_discarded_gaps(self):
        # Window: 09:00 - 18:00
        busy = [
            (self.base + timedelta(hours=1), self.base + timedelta(hours=2)), # 10:00 - 11:00
            # Creates a 4-minute gap from 11:00 to 11:04
            (self.base + timedelta(hours=2, minutes=4), self.base + timedelta(hours=3)) # 11:04 - 12:00
        ]
        
        result = calculate_availability(self.base, self.window_end, busy)
        
        # Block 1: 09:00 - 10:00 (1 hour)
        # Block 2: 12:00 - 18:00 (6 hours)
        self.assertEqual(len(result["free_blocks"]), 2)
        
        # 4 minute gap should be logged in discarded
        self.assertEqual(result["discarded_gaps_time"], timedelta(minutes=4))
        
        # Total Busy Time = 1h + 56m = 1h 56m
        self.assertEqual(result["consolidated_busy_time"], timedelta(hours=1, minutes=56))

    def test_calculate_availability_fully_busy(self):
        busy = [(self.base, self.window_end)]
        result = calculate_availability(self.base, self.window_end, busy)
        self.assertEqual(len(result["free_blocks"]), 0)
        self.assertEqual(result["total_available_time"], timedelta(0))
        self.assertEqual(result["consolidated_busy_time"], timedelta(hours=9))

if __name__ == '__main__':
    unittest.main()
