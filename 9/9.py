from common import Node
from typing import List, Set, Tuple

data = open('./input')
lines = data.readlines()
data.close()

# part 1
head = Node()
tail = Node()

positions_of_tail: Set[Tuple[int, int]] = set()

for line in lines:
    direction, count = line.strip().split(' ')
    count = int(count)
    while count > 0:
        head.move[direction]()
        tail.follow(head)
        positions_of_tail.add((tail.x, tail.y))
        count -= 1

print(f'(part 1) unique positions = {len(positions_of_tail)}')

# part 2
rope: List[Node] = [Node() for _ in range(10)]
head = rope[0]
for i, node in enumerate(rope[:-1]):
    node.next = rope[i+1]
tail = rope[-1]

positions_of_tail: Set[Tuple[int, int]] = set()

for line in lines:
    direction, count = line.strip().split(' ')
    count = int(count)
    while count > 0:
        head.move[direction]()
        for node in rope[:-1]:
            node.next.follow(node)
        positions_of_tail.add((tail.x, tail.y))
        count -= 1

print(f'(part 2) unique positions = {len(positions_of_tail)}')
