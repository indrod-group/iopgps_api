from typing import Optional, Tuple
from django.utils import timezone

def fix_range_times(
    start_time: Optional[int], end_time: Optional[int]
) -> Tuple[int, int]:
    """
    This function adjusts the start and end times to a valid range.
    If either of the times is None, it will be replaced with a default value.
    The start time defaults to the timestamp of the start 
    of the current day, and the end time defaults to the current timestamp.
    If the end time is earlier than the start time,
    they will be swapped to ensure a valid range.

    Args:
        - start_time (Optional[int]): The start time as a Unix timestamp. 
            If None, it will be replaced with the timestamp of the start of the current day.
        - end_time (Optional[int]): The end time as a Unix timestamp.
            If None, it will be replaced with the current timestamp.

    Returns:
        - Tuple[int, int]: A tuple containing the adjusted start and end times as Unix timestamps.
    """
    if start_time is None:
        start_time: int = int(
            timezone.now()
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )
    else:
        start_time = int(start_time)

    if end_time is None:
        end_time = int(timezone.now().timestamp())
    else:
        end_time = int(end_time)

    if end_time < start_time:
        start_time, end_time = end_time, start_time

    return start_time, end_time
