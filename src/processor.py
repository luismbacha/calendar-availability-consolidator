from datetime import datetime, timedelta

def merge_intervals(intervals: list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
    """
    Merges overlapping or adjacent datetime intervals using an O(N log N) sweep-line algorithm.
    """
    if not intervals:
        return []
    
    # Sort intervals primarily by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current_start, current_end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]

        if current_start <= last_end:
            # Intervals overlap or are immediately adjacent; extend the last merged interval
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # Intervals are completely disjoint; add as a new block
            merged.append((current_start, current_end))

    return merged

def calculate_availability(window_start: datetime, window_end: datetime, busy_intervals: list[tuple[datetime, datetime]]) -> dict:
    """
    Calculates free time blocks by inverting the merged busy intervals against the requested window.
    Discards free blocks strictly less than 5 minutes.
    """
    merged_busy = merge_intervals(busy_intervals)
    
    # Clip merged busy intervals to strictly fit within the requested window bounds
    clipped_busy = []
    for b_start, b_end in merged_busy:
        c_start = max(window_start, b_start)
        c_end = min(window_end, b_end)
        if c_start < c_end:
            clipped_busy.append((c_start, c_end))

    free_blocks = []
    discarded_duration = timedelta()
    consolidated_busy_duration = sum((end - start for start, end in clipped_busy), timedelta())
    
    current_time = window_start

    for b_start, b_end in clipped_busy:
        if current_time < b_start:
            gap = b_start - current_time
            if gap >= timedelta(minutes=5):
                free_blocks.append((current_time, b_start))
            else:
                discarded_duration += gap
        # Advance the pointer to the end of the current busy block
        current_time = max(current_time, b_end)

    # Check for a final free block after the last busy interval up to the window end
    if current_time < window_end:
        gap = window_end - current_time
        if gap >= timedelta(minutes=5):
            free_blocks.append((current_time, window_end))
        else:
            discarded_duration += gap

    total_available_duration = sum((end - start for start, end in free_blocks), timedelta())

    return {
        "free_blocks": free_blocks,
        "total_available_time": total_available_duration,
        "consolidated_busy_time": consolidated_busy_duration,
        "discarded_gaps_time": discarded_duration
    }
