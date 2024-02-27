from __future__ import annotations


class Point:
    def __init__(self, x: str, y: str, z: str) -> None:
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    def touching(self, other: Point):
        if (abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)) == 1:
            return True


points = []

with open('./input') as data:
    for line in data:
        coord = line.strip().split(',', 3)
        points.append(Point(*coord))

# part 1
total_sides = len(points) * 6

for i, point in enumerate(points):
    for other in points[i:]:
        if point.touching(other):
            total_sides -= 2

print(f'total sides exposed = {total_sides}')

# part 2
