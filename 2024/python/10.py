from collections import namedtuple

with open('../inputs/10.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

# represents a position
Coords = namedtuple('Coords', ['x', 'y'])
# save all heights and starting positions
map_data: list[list[int]] = []
start_positions: list[Coords] = []
for x, line in enumerate(input):
    map_data.append([])
    for y, height in enumerate(line.strip()):
        height = int(height)
        map_data[x].append(height)
        # this is a start position
        if height == 0:
            start_positions.append(Coords(x, y))
max_x = len(input) - 1
max_y = len(input[0].strip()) - 1  # all lines same len
assert (max_x == max_y)

###############
# utils
###############

# should i make a utils folder for all this repeating stuff?


def _in_bounds(position: Coords) -> bool:
    """Check whether the current position is in bounds.
    Parameters
        position: the current position as a 2d vector

    Returns
        True if in bounds, False otherwise
    """
    return (0 <= position.x <= max_x) and (0 <= position.y <= max_y)


def get_neighbors(position: Coords) -> set[Coords]:
    """Returns neighbors of the current position. A cell can have
    2, 3 or 4 neighbors.

    Parameters
        pos: the starting position

    Returns
        a list with the coordinates of the neighbors
    """
    neighbors = set()
    # all the possible directions, no diagonals
    increments = (-1, 1)
    for dx in increments:
        candidate = Coords(position.x+dx, position.y)
        if _in_bounds(candidate):
            neighbors.add(candidate)
    for dy in increments:
        candidate = Coords(position.x, position.y+dy)
        if _in_bounds(candidate):
            neighbors.add(candidate)
    return neighbors

###############
# part 1 & 2
###############


ratings: int = 0
trailheads_score: int = 0
# for every starting position, iteratevely check neighbors
# and follow a path of increasing height
for start in start_positions:
    # start from height 0
    curr_height = 0
    neighbors = get_neighbors(start)
    # check all neighbors and keep only the ones with correct height
    # exit early if i can't find any neighbors that respect the condition
    neighbors = set(
        filter(lambda c: map_data[c.x][c.y] == curr_height+1, neighbors))
    curr_height += 1
    while curr_height < 9 and len(neighbors) >= 0:
        # next step is one up
        # update neighbors with the neighbors of the current ones
        new_neighbors = []
        for neighbor in neighbors:
            new_neighbors += list(get_neighbors(neighbor))
        # remove the ones that do not fulfil height requirements
        neighbors = list(
            filter(lambda c: map_data[c.x][c.y] == curr_height+1, new_neighbors))
        curr_height += 1
    # for part 1 i just count the unique destinations
    # for part 2 i count all different paths
    # neighbors is empty if the path is a dead end
    trailheads_score += len(set(neighbors))
    ratings += len(neighbors)

print(f'part 1: {trailheads_score}')
print(f'part 2: {ratings}')
