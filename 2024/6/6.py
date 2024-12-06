from __future__ import annotations
from time import time

with open('./input') as data:
    input = data.readlines()

###############
# input parsing
###############


class Vector2D:
    """Helper class to define positions and steps in the grid.
    Can encode a position in 2d or a direction.
    Position (0, 0) is top left and the x represents lines and y
    represents columns.

    Attributes
        x: the x position
        y: the y position
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Vector2D):
            return False
        return self.x == value.x and self.y == value.y

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        # needed to use positions as dictionary keys
        return hash((self.x, self.y))

    def __add__(self, value: object) -> Vector2D:
        if not isinstance(value, Vector2D):
            raise ValueError('can only sum two positions')
        return Vector2D(self.x+value.x, self.y+value.y)


# save starting position (^, facing up)
start: Vector2D
# keep track of obstacles positions
obstacles: set[Vector2D] = set()
# bounds
max_x = len(input) - 1
max_y = len(input[0]) - 1  # all lines same len
for x, line in enumerate(input):
    for y, char in enumerate(line):
        if char == '#':
            obstacles.add(Vector2D(x, y))
        if char == '^':
            start = Vector2D(x, y)


###############
# helpers
###############


# steps in order of rotation
# a bit unintuitive since 0,0 is in top left
# then x is the line number and y the column number
class Steps:
    up = Vector2D(-1, 0)
    right = Vector2D(0, 1)
    down = Vector2D(1, 0)
    left = Vector2D(0, -1)


steps: Steps = Steps()

# direction to turn to given the current direction
turn: dict[Vector2D, Vector2D] = {
    steps.up: steps.right,
    steps.right: steps.down,
    steps.down: steps.left,
    steps.left: steps.up
}


def in_bounds(position: Vector2D) -> bool:
    """Check whether the current position is in bounds.
    Parameters
        position: the current position as a 2d vector

    Returns
        True if in bounds, False otherwise
    """
    return (0 <= position.x <= max_x) and (0 <= position.y <= max_y)


###############
# part 1
###############


# start from initial position going up
position: Vector2D = start
current_direction: Vector2D = steps.up
# keep track of visited places
visited_places: set[Vector2D] = set()
# as long as i stay in bounds, continue moving
while (in_bounds(position)):
    visited_places.add(position)
    next_position: Vector2D = position + current_direction
    # while loop since i can turn up to two times in a row
    while next_position in obstacles:
        # i am facing an obstacle, turn
        current_direction = turn[current_direction]
        next_position = position + current_direction
    position = next_position

print(f'part 1: {len(visited_places)}')


###############
# part 2
###############

# idea for infinite loop:
# if i visit again a position that was visited and the
# direction i am going is the same as last time it means
# that i will be looping since behaviour is deterministic
# to find all possible obstacle position i could bruteforce,
# add a new obstacle at a time in each position and check
# for loops, but that would be long. I could save time
# by just putting the obstacles at each position that it is traversed
# by the guard and check only those, but that's just about a 3.3x
# reduction in checks (5129 vs 17030 for my input)
# the ideal way would be to track if the current path will intersect
# with another one and place an obstacle that would make it turn
# in the same direction again (need to keep track of position and
# directions) but i am lazy

# possible obstacles to add
obstacles_to_make_loops: set[Vector2D] = set()
# keep track of time
sum: float = 0.0
# reuse visited places from before
for candidate in visited_places:
    begin = time()
    new_obstacle: Vector2D = candidate
    if new_obstacle in obstacles:
        # skip this one, since it's already present
        continue
    # add to the set of obstacles
    obstacles.add(new_obstacle)
    # simulate the path with the new obstacle and
    # check for loops
    # start from initial position going up
    position: Vector2D = start
    current_direction: Vector2D = steps.up
    # keep track of visited places and the direction that i was
    # going when passing through it
    visited_places_with_direction: set[tuple[Vector2D, Vector2D]] = set()
    # flag to check for loop
    looping: bool = False
    while (in_bounds(position) and not looping):
        # keep track of position and direction
        new_position_direction = (position, current_direction)
        if new_position_direction in visited_places_with_direction:
            # if it is already present i am in a loop, exit
            looping = True
            break
        # otherwise, keep going
        visited_places_with_direction.add(new_position_direction)
        next_position: Vector2D = position + current_direction
        # here the logic is the same as part 1
        while next_position in obstacles:
            # i am facing an obstacle, turn
            current_direction = turn[current_direction]
            next_position = position + current_direction
        position = next_position
    # if i found a loop, add the new obstacle to the list
    if looping:
        obstacles_to_make_loops.add(new_obstacle)
    # at the end remove the obstacle
    obstacles.remove(new_obstacle)
    # time tracking
    end = time()
    sum += end-begin

# about 20 seconds on my machine, single core
print(f'average time per iteration {
      (sum/len(visited_places)):.3f}s, total = ({sum:.3f})')

print(f'part 2: {len(obstacles_to_make_loops)}')
