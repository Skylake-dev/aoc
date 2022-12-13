import json
from typing import List
from common import (
    right_order
)

data = open('./input')

left = []
right = []

line = data.readline()

while line != '':
    left.append(json.loads(line))
    line = data.readline()
    right.append(json.loads(line))
    data.readline()  # skip white line
    line = data.readline()

data.close()

assert len(left) == len(right)
right_order_indexes: List[int] = []

for i, left_packet in enumerate(left):
    right_packet = right[i]
    if right_order(left_packet, right_packet):
        right_order_indexes.append(i+1)

print(f'Total indexes in right order = {sum(right_order_indexes)}')
