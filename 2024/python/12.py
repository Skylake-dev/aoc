from time import time
from collections import namedtuple
from dataclasses import dataclass

with open('../inputs/12.txt') as data:
    # with open('../inputs/12.txt') as data:
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


def get_same_type_neighbors_horizontally(pos: Coords) -> list[Coords]:
    """Get the neighbors left and right of this cell, if any."""
    neighbors = []
    increments = (-1, 1)
    # left and right means fix row and move column
    for dy in increments:
        cand = Coords(pos.x, pos.y+dy)
        # short circuit the and if not in bounds
        if _in_bounds(cand) and plots_map[pos.x][pos.y] == plots_map[cand.x][cand.y]:
            neighbors.append(cand)
    return neighbors


def get_same_type_neighbors_vertically(pos: Coords) -> list[Coords]:
    """Get the neighbors above and below this cell, if any."""
    neighbors = []
    increments = (-1, 1)
    # above and below means fix the column and move row
    for dx in increments:
        cand = Coords(pos.x+dx, pos.y)
        if _in_bounds(cand) and plots_map[pos.x][pos.y] == plots_map[cand.x][cand.y]:
            neighbors.append(cand)
    return neighbors


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
    neighbors += get_same_type_neighbors_horizontally(pos)
    neighbors += get_same_type_neighbors_vertically(pos)
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
    plots: set[Coords]          # plots of the garden in this area
    label: str = ''             # the type of plots inside this region
    perimeter: int = 0          # the perimeter, invalid value until the end
    sides: int = 0              # the number of sides, same as perimeter but merge contiguous
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


def build_contiguous_sections(points: list[int]) -> list[list[int]]:
    # first extract contiguous blocks by checking delta between points
    if len(points) == 0:
        # empty, so return empty list
        return []
    contiguous_sections: list[list[int]] = [[points[0]]]
    for i in range(1, len(points)):
        if points[i] == points[i-1] + 1:
            # it's contiguous, keep appending to the current array
            contiguous_sections[-1].append(points[i])
        else:
            # not contiguous, create a new block
            contiguous_sections.append([points[i]])
    return contiguous_sections

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
    # ok this is a weird idea, but
    # i could divide the points in two dictionary, one
    # indexed by the x coord and the other by the y coord
    # and then sort the other coordinate and extract contiguous
    # groups
    x_map: dict[int, list[int]] = {}
    y_map: dict[int, list[int]] = {}
    for plot in border_plots:
        # add points from the x
        if plot.x in x_map:
            x_map[plot.x].append(plot.y)
        else:
            x_map[plot.x] = [plot.y]
        # add points from the y
        if plot.y in y_map:
            y_map[plot.y].append(plot.x)
        else:
            y_map[plot.y] = [plot.x]
    # track the number of sides, see comments later to
    # understand the procedure
    above_sides: int = 0
    below_sides: int = 0
    left_sides: int = 0
    right_sides: int = 0
    for x in x_map:
        # sort them all in order of coordinates, so that it would
        # be easier to extract the contiguous plots
        points = x_map[x]
        points.sort()
        # assume they all form one side and split them when needed
        # e.g. in a square region for one i have either the top or bottom
        # side not both in the same lines
        # this is used to handle plots that protrude out, for instance when
        # considering this region
        # S S S S
        # S S S
        # check the first line, both above and below
        # _ _ _ _   --> 1 contiguous side
        # S S S S
        # x x x _   --> 1 contiguous side but short, blocked by neighbors below
        # S S S
        # but for the second line, the side above are all blocked
        # S S S S
        # x x x     --> 1 contiguous side but blocked by neighbors above, so no side is added
        # S S S
        # _ _ _     --> 1 contiguous side
        contiguous_plots = build_contiguous_sections(points)
        # now check the neigbors for blocking for each of the contiguous plots
        # blockings will cause more splits within each contiguous side
        # the blocking is tracked in a list of booleans, and this will be used to
        # determine the split
        # e.g.
        # blocked_above = [True, False, False]
        # blocked_below = [False, False, False]
        # represents something like
        #  S
        #  S S S   <-- considering this line
        # so the considered line will have one side above and one below
        # a split is caused by a section of True between False
        # e.g.
        # blocked_above = [False, True, False]
        # blocked_below = [False, False, False]
        # represents something like
        #    S
        #  S S S   <-- considering this line
        # below there will be a single side like before, but above
        # i have a split caused by the S in the middle, so it will
        # produce 2 sides (for this line, the third side caused by the
        # above S will be handled by that line)

        for section in contiguous_plots:
            blocked_above: list[bool] = []
            blocked_below: list[bool] = []
            for cell_y in section:
                # only interested in the x coordinate
                vertical_neighbors: list[int] = list(
                    map(lambda pos: pos.x, get_same_type_neighbors_vertically(Coords(x, cell_y))))
                # track blocked cells above and below (remember the weird axis of row column)
                blocked_below.append((x + 1) in vertical_neighbors)
                blocked_above.append((x - 1) in vertical_neighbors)
            # now produce the split of this section, counting the sides
            # to produce the splits filter out the elements that are blocked
            # do the splits
            unblocked_cells_above = [section[i] for i in range(
                len(section)) if not blocked_above[i]]
            unblocked_cells_below = [section[i] for i in range(
                len(section)) if not blocked_below[i]]
            # if it was not split, this should only add 1, if all are blocked then
            # no side is counted for that part
            above_sides += len(build_contiguous_sections(unblocked_cells_above))
            below_sides += len(build_contiguous_sections(unblocked_cells_below))
    # do the same thing on y but check left/right neighbors instead
    # see the logic in the previous comments
    for y in y_map:
        points = y_map[y]
        points.sort()
        contiguous_plots = build_contiguous_sections(points)
        for section in contiguous_plots:
            blocked_left: list[bool] = []
            blocked_right: list[bool] = []
            for cell_x in section:
                # only interested in the y coordinate this time
                horizontal_neighbors: list[int] = list(
                    map(lambda pos: pos.y, get_same_type_neighbors_horizontally(Coords(cell_x, y))))
                blocked_right.append((y + 1) in horizontal_neighbors)
                blocked_left.append((y - 1) in horizontal_neighbors)
            unblocked_cells_left = [section[i] for i in range(
                len(section)) if not blocked_left[i]]
            unblocked_cells_right = [section[i] for i in range(
                len(section)) if not blocked_right[i]]
            left_sides += len(build_contiguous_sections(unblocked_cells_left))
            right_sides += len(build_contiguous_sections(unblocked_cells_right))
    # the sides of the region is the sum of all of these sides
    region.sides = above_sides + below_sides + left_sides + right_sides

print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {sum([r.area*r.sides for r in regions])}')
