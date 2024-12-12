from time import sleep
from time import time
from collections import namedtuple
from dataclasses import dataclass, field

with open('../inputs/12.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

# hey look a 2d matrix, how original
# store all the plots at the correct coord
plots_map: list[list[str]] = []
for x, line in enumerate(input):
    plots_map.append([])
    for char in line.strip():
        plots_map[x].append(char)

# bounds
max_x = len(input) - 1
# need to strip out \n otherwise it's wrong
max_y = len(input[0].strip()) - 1  # all lines same len

# store a flag for each plot to check whether it is assigned to a region or not
# i could have better locality by storing a tuple with the (label, flag)
assigned: list[list[bool]] = [
    [False for _ in range(max_y+1)] for _ in range(max_x+1)]

###############
# utils
###############

# the answer to the question in day 10 is yes
# will i do it? no(t yet, maybe)
Coords = namedtuple('Coords', ['x', 'y'])


def _in_bounds(point: Coords) -> bool:
    """Check whether the current point is in bounds.
    Parameters
        point: the point to check

    Returns
        True if in bounds, False otherwise
    """
    return (0 <= point.x <= max_x) and (0 <= point.y <= max_y)


def get_same_type_neighbors(pos: Coords) -> list[Coords]:
    """Returns neighbors of the current position. A cell can have
    between 0 and 4 neighbors (since we exclude diagonals).
    A cell is considered neighbor only if it of the same type,
    i.e. same letter that there is in the given postion.

    Parameters
        pos: the starting position

    Returns
        a list with the coordinates of the neighbors
    """
    neighbors = []
    # all the possible directions, no diagonals
    # check bounds and that the type is the same
    # before appending the neighbor
    increments = (-1, 1)
    for dx in increments:
        cand = Coords(pos.x+dx, pos.y)
        if _in_bounds(cand) and plots_map[pos.x][pos.y] == plots_map[cand.x][cand.y]:
            neighbors.append(cand)
    for dy in increments:
        cand = Coords(pos.x, pos.y+dy)
        if _in_bounds(cand) and plots_map[pos.x][pos.y] == plots_map[cand.x][cand.y]:
            neighbors.append(cand)
    return neighbors


def get_same_type_unassigned_neighbors(pos: Coords) -> list[Coords]:
    """Same as `get_same_type_neighbors` but filter out assigned plots.

    Parameters
        pos: the starting position

    Returns
        a list with the coordinates of the neighbors
    """
    return list(filter(lambda p: not assigned[p.x]
                       [p.y], get_same_type_neighbors(pos)))


@dataclass
class Region:
    # define a region, containing different fields
    # set is not initialized because i was having errors
    plots: set[Coords]          # plots of the garden in this area
    label: str = ''             # the type of plots inside this region
    perimeter: int = 0          # the perimeter, invalid value until the end
    area: int = 0               # the area, which is just the number of plots


def recursive_neighbor_update(region: Region, neighbors: list[Coords]) -> None:
    """Recursively create a region by following the neighbors."""
    if neighbors == []:
        # exit condition
        return
    # add cells to the region
    region.plots.update(neighbors)
    # flag them
    for cell in neighbors:
        assigned[cell.x][cell.y] = True
    # recursively do this for each neighbor, only the ones not assigned
    for cell in neighbors:
        recursive_neighbor_update(
            region, get_same_type_unassigned_neighbors(cell))


###############
# part 1
###############


# i need perimeter and area of each region, so first i must map out all the regions
# a region is a set of cells that are all neighbors, according to the description
# given in the (self explainatory) `get_same_type_neighbors` function
# to compute the cost we need, for each region:
# - perimeter is the sum of (4-number of neighbors) for each cell in a region
# - area is the number of cells in that region
# then the cost is the sum of area*perimeter for all regions
# track time
begin: float = time()
# store regions in a list
regions: list[Region] = []
for x in range(max_x+1):
    for y in range(max_y+1):
        if assigned[x][y]:
            # i already assigned this plot, skip
            continue
        # get the current plot type
        label = plots_map[x][y]
        # this was not assigned to any region, so create a new region
        # with this cell. compute perimeter and area at the end
        region = Region(label=label, plots=set(
            [Coords(x, y)]))
        # flag this cell as assigned
        assigned[x][y] = True
        # build the region by searching neighbors of the same type and
        # add them here, keep updating area and perimeter
        # only check unassigned neighbors
        neighbors = get_same_type_unassigned_neighbors(Coords(x, y))
        # build the region
        recursive_neighbor_update(region, neighbors)
        # can compute area now
        region.area = len(region.plots)
        # compute the perimeter
        # for each cell in the region, add 4 and subtract the number
        # of touching cells (neighbors)
        for cell in region.plots:
            region.perimeter += 4 - len(get_same_type_neighbors(cell))
        regions.append(region)

print(f'[part 1] time: {(time()-begin):.4f}s')
print(f'part 1: {sum([r.area*r.perimeter for r in regions])}')

###############
# part 2
###############

# track time
begin: float = time()
for region in regions:
    # i already have the regions, filter out just the border
    # plots, i.e. the ones with less than 4 neighbors
    border_plots = list(filter(lambda p: len(
        get_same_type_neighbors(p)) < 4, region.plots))
    # need to figure out logic

print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {0}')
