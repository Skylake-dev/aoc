from itertools import combinations
from collections import namedtuple

with open('./input') as data:
    input = data.readlines()

###############
# input parsing
###############

Coords = namedtuple('Coords', ['x', 'y'])

# antennas stored in a dictionary with
# symbol: (location1, location2, ...)
antennas: dict[str, set[Coords]] = {}
for x, line in enumerate(input):
    for y, char in enumerate(line.strip()):
        if char != '.':
            if char in antennas:
                antennas[char].add(Coords(x, y))
            else:
                antennas[char] = set([Coords(x, y)])
# bounds
max_x = len(input) - 1
# need to strip out \n otherwise it's wrong (took me 20 minutes to figure out that
# this was the problem...)
max_y = len(input[0].strip()) - 1  # all lines same len

###############
# utils
###############


def _central_symmetry(point: Coords, center: Coords) -> Coords:
    """Computes the symmetric point given a point and a center."""
    return Coords(2*center.x - point.x, 2*center.y - point.y)


def _in_bounds(point: Coords) -> bool:
    """Check whether the current point is in bounds.
    Parameters
        point: the point to check

    Returns
        True if in bounds, False otherwise
    """
    return (0 <= point.x <= max_x) and (0 <= point.y <= max_y)


def get_antinodes_in_bounds(a1: Coords, a2: Coords) -> tuple[Coords, ...]:
    """Compute the antinodes given two antennas. Only returns antinodes that
    are within the bounds of the map, so 0, 1 or 2 coordinates may be returned.

    Parameters:
        a1: the coordinates of the first antenna
        a2: the coordinates of the second antenna

    Returns:
        a tuple with the coordinates of the antinodes that are in bounds,
        can be empty
    """
    return tuple(filter(_in_bounds, (_central_symmetry(a1, a2), _central_symmetry(a2, a1))))


def _antinode_and_harmonics(a1: Coords, a2: Coords) -> list[Coords]:
    # helper to compute iteratively the harmonics
    # the two antennas will also produce a new harmonic at their location
    antinodes: list[Coords] = [a1, a2]
    # temporary variables for the loop
    point: Coords = a1
    center: Coords = a2
    anti = _central_symmetry(point, center)
    while _in_bounds(anti):
        antinodes.append(anti)
        point = center
        center = anti
        anti = _central_symmetry(point, center)
    return antinodes


def get_antinodes_and_harmonics_in_bounds(a1: Coords, a2: Coords) -> tuple[Coords, ...]:
    """Compute the antinodes given two antennas. Takes into account harmonics,
    so it may return any number of antinodes (even 0). Only considers the ones in bounds

    Parameters:
        a1: the coordinates of the first antenna
        a2: the coordinates of the second antenna

    Returns:
        a tuple with the coordinates of the antinodes that are in bounds,
        can be empty
    """
    antinodes: list[Coords] = []
    # compute antinodes and harmonics in both directions
    antinodes += _antinode_and_harmonics(a1, a2)
    antinodes += _antinode_and_harmonics(a2, a1)
    # i don't need to check bounds since i already did that in the function
    # return tuple(filter(_in_bounds, (_central_symmetry(a1, a2), _central_symmetry(a2, a1))))
    return tuple(antinodes)


###############
# part 1 & 2
###############

# for all possible types of antennas compute the antinodes
# between each pair and count the unique items
antinodes: set[Coords] = set()
# also do part 2 here, track the harmonics
antinodes_with_harmonics: set[Coords] = set()
for antenna_type in antennas:
    # get all pairs (combinations is empty if i only have 1 antenna)
    for pair in combinations(antennas[antenna_type], 2):
        antinodes.update(get_antinodes_in_bounds(*pair))
        antinodes_with_harmonics.update(
            get_antinodes_and_harmonics_in_bounds(*pair))

print(f'part 1: {len(antinodes)}')
print(f'part 1: {len(antinodes_with_harmonics)}')
