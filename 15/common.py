from typing import List, NamedTuple, Optional, Tuple


class Interval(NamedTuple):
    start: int
    end: int


class Beacon(NamedTuple):
    x: int
    y: int


class Sensor:
    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.beacon_x: int = beacon_x
        self.beacon_y: int = beacon_y
        self.radius: int = self.distance_from_beacon(
            self.beacon_x, self.beacon_y)

    def distance_from_beacon(self, beacon_x: int, beacon_y: int) -> int:
        return abs(self.x - beacon_x) + abs(self.y - beacon_y)

    def distance_from_row(self, y_row: int) -> int:
        return abs(y_row - self.y)

    def cells_covered_in_row(self, y_row: int) -> Tuple[int, int, int]:
        distance = self.radius - self.distance_from_row(y_row)
        if distance < 0:
            # outside radius
            return (0, 0, 0)
        else:
            # inside radius, compute covered cells
            # cells_covered = 1 + 2*distance if doesn't go out border
            start = self.x - distance
            end = self.x + distance
            cells_covered = end - start + 1
            return (cells_covered, start, end)


# remember day 4?
def _contained(int1: Interval, int2: Interval) -> bool:
    return (int1.start >= int2.start and int1.end <= int2.end) or (int2.start >= int1.start and int2.end <= int1.end)


def _overlap(int1: Interval, int2: Interval) -> bool:
    if _contained(int1, int2):
        return True
    return (int1.end > int2.end >= int1.start > int2.start) or (int2.end > int1.end >= int2.start > int1.start)


def interval_len(int: Interval) -> int:
    return int.end - int.start + 1


def _recursive_overlap(intervals: List[Interval], new_int: Interval) -> None:
    overlaps = False
    for i, interval in enumerate(intervals):
        if _overlap(new_int, interval):
            start = min(new_int.start, interval.start)
            end = max(new_int.end, interval.end)
            new_int = Interval(start, end)
            overlaps = True
            intervals.pop(i)   # i can remove it because i break cycle
            break
    if overlaps:
        _recursive_overlap(intervals, new_int)
    else:
        intervals.append(new_int)


def add_interval(intervals: List[Interval], new_int: Interval) -> None:
    if not intervals:
        intervals.append(new_int)
    _recursive_overlap(intervals, new_int)


def find_empty(intervals: List[Interval], MIN: int, MAX: int, target_y_row: int) -> Optional[Tuple[int, int]]:
    if len(intervals) == 1:
        # free space can be only in start or end
        if intervals[0].start <= MIN and intervals[0].end >= MAX:
            return None
        if intervals[0].start == MIN:
            x = MIN
        else:
            x = MAX
        return (x, target_y_row)
    else:
        # if a have more than one interval, the holes are when they separate
        # otherwise they would have been merged before
        # assume at most 1 hole
        return (intervals[0].end+1, target_y_row)
