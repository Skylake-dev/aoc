import json
import functools
from typing import List
from common import (
    right_order
)

packets = []
with open('./input') as data:
    for line in data:
        if line == '\n' or line == '\r\n':
            continue
        packets.append(json.loads(line))

# add distress packets
distress_packets = ([[2]], [[6]])
for packet in distress_packets:
    packets.append(packet)


def comparator(x, y) -> int:
    result = right_order(x, y)
    if result is True:
        return -1  # right order, do not swap
    elif result is False:
        return 1   # wrong order, swap
    else:
        return 0


# just do a simple sort
packets.sort(key=functools.cmp_to_key(comparator))

# spot the dividers
divider_indexes: List[int] = []
for i, packet in enumerate(packets):
    if packet in distress_packets:
        divider_indexes.append(i+1)

print(
    f'Decoding key = {functools.reduce((lambda i1, i2: i1*i2), divider_indexes)}')
