import re
from common import (
    Interval,
    Beacon,
    Sensor,
    add_interval,
    interval_len,
    find_empty
)
from typing import List, Optional, Set, Tuple

sensors: List[Sensor] = []
beacons: Set[Beacon] = set()
with open('./input') as data:
    for line in data:
        coords = [int(c) for c in re.findall(r'[-]?\d+', line)]
        sensor = Sensor(*coords)
        sensors.append(sensor)
        beacons.add(Beacon(sensor.beacon_x, sensor.beacon_y))

# part 1
target_y_row = 2000000
intervals: List[Interval] = []
for sensor in sensors:
    n_cells, min_x, max_x = sensor.cells_covered_in_row(target_y_row)
    if n_cells != 0:
        add_interval(intervals, Interval(min_x, max_x))  # deal with overlaps

count = sum(interval_len(int1) for int1 in intervals)
# remove beacons on that line
occupied = sum(1 for b in beacons if b.y == target_y_row)
count -= occupied

print(f'cells covered = {count}')

# part 2
MIN = 0
MAX = 4000000
free_spot: Optional[Tuple[int, int]] = None
target_y_row = MIN
print('this will take a minute...')
while target_y_row <= MAX:
    intervals: List[Interval] = []
    for sensor in sensors:
        n_cells, min_x, max_x = sensor.cells_covered_in_row(target_y_row)
        if n_cells != 0:
            add_interval(intervals, Interval(min_x, max_x))
    free_spot = find_empty(intervals, MIN, MAX, target_y_row)
    if free_spot:
        break
    else:
        target_y_row += 1

if free_spot:
    tuning_freq = MAX*free_spot[0] + free_spot[1]
    print(f'tuning frequency = {tuning_freq}')
