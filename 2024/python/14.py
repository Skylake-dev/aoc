from __future__ import annotations
from statistics import variance
import re
from time import time
from dataclasses import dataclass

with open('../inputs/14.txt') as data:
    input_file = data.readlines()

###############
# input parsing
###############

# again, i need a library for this
# this time +x is right, -x is left
# and +y is down and -y is up
GRID_X_WIDTH: int = 101
GRID_Y_TALL: int = 103


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
        self.x = x % GRID_X_WIDTH
        self.y = y % GRID_Y_TALL

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Vector2D):
            return False
        return self.x == value.x and self.y == value.y

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, value: object) -> Vector2D:
        if not isinstance(value, Vector2D):
            raise ValueError('can only sum two positions')
        # add in modulus, so it wraps around the map
        return Vector2D(self.x+value.x % GRID_X_WIDTH, self.y+value.y % GRID_Y_TALL)

    def __mul__(self, value: object) -> Vector2D:
        if not isinstance(value, int):
            raise ValueError('can only multiply integer scalar with vector')
        # stay in map
        return Vector2D((self.x*value) % GRID_X_WIDTH, (self.y*value) % GRID_Y_TALL)


# regex to parse integers from the line, with sign
integer = r'-?[0-9]+'
integer = re.compile(integer)


@dataclass
class Robot:
    # helper for each robot
    position: Vector2D
    speed: Vector2D

    def __str__(self) -> str:
        return f'Robot(position: {str(self.position)}, speed: {str(self.speed)})'

    def __repr__(self) -> str:
        return self.__str__()


bots: list[Robot] = []

for line in input_file:
    # postion and velocity for each robot are just numbers
    ints = list(map(int, re.findall(integer, line)))
    if ints == []:
        # last line is empty
        break
    bots.append(Robot(Vector2D(ints[0], ints[1]), Vector2D(ints[2], ints[3])))

###############
# part 1
###############

# track time
begin: float = time()
SECONDS: int = 100
# track the final position after `SECONDS` iteration
end_positions: list[Vector2D] = []
for bot in bots:
    end_positions.append(bot.position + (bot.speed*SECONDS))
# count bots in each quadrant, assume at least 1 in each quadrant
safety_factor: int = 1
# add up all the quadrants, excluding middle line
safety_factor *= len(list(filter(lambda pos: pos.x < (GRID_X_WIDTH // 2)
                     and pos.y < (GRID_Y_TALL // 2), end_positions)))
safety_factor *= len(list(filter(lambda pos: pos.x > (GRID_X_WIDTH // 2)
                     and pos.y < (GRID_Y_TALL // 2), end_positions)))
safety_factor *= len(list(filter(lambda pos: pos.x < (GRID_X_WIDTH // 2)
                     and pos.y > (GRID_Y_TALL // 2), end_positions)))
safety_factor *= len(list(filter(lambda pos: pos.x > (GRID_X_WIDTH // 2)
                     and pos.y > (GRID_Y_TALL // 2), end_positions)))
print(f'[part 1] time: {(time()-begin):.4f}s')
print(f'part 1: {safety_factor}')

###############
# part 2
###############

# no need to track time
# def pretty_print(bots: list[Robot]) -> str:
#     grid: str = ''
#     positions: set[Vector2D] = set([b.position for b in bots])
#     for x in range(GRID_Y_TALL):
#         for y in range(GRID_X_WIDTH):
#             if Vector2D(x, y) in positions:
#                 grid += '#'
#             else:
#                 grid += '.'
#         grid += '\n'
#     return grid
# wtf are the requirements, i will just pretty print and go manually?
# i guess the other alternative would be to write a general christmas tree finder
# or ask an image classificator if it sees a christmas tree
# print(f'''You will see a sequence of grid of {GRID_X_WIDTH}x{GRID_Y_TALL} squares
# Make sure that your terminal can see this size because you will have to find a tree
# inside this picture. Keep going until you see a christmas tree.
# Should not take more than 100 iterations, otherwise start to worry.''')
# input('Press enter to continue...')
# seconds_needed: int = 0
# while True:
#     print(pretty_print(bots))
#     print(f'[Elapsed seconds: {seconds_needed}]')
#     input('Do you see a christmas tree? Press enter to continue...')
#     seconds_needed += 1
#     bots = [Robot(b.position + b.speed, b.speed) for b in bots]

# NOTE: what i saw during this is that the position get "clustered" where i can see
# the positions mostly aligned vertically or mostly aligned horizontally
# so the guess is that when both are clustered there would be the tree
# if this doesn't work then rip
# to estimate the "clustering" i look at the variances on both axis
# i tried computing the least common multiple but the solution was wrong...

# track time
begin: float = time()
seconds_needed: int = 0
while True:
    var_x = variance(b.position.x for b in bots)
    var_y = variance(b.position.y for b in bots)
    if var_x < 500.0 and var_y < 500.0:
        print(f'[{seconds_needed}] var x = {var_x}, var y = {var_y}')
        print(seconds_needed)
        break
    # this was used to tune the threshold lol
    # if var_x < 500.0 or var_y < 500.0:
    #     print(f'[{seconds_needed}] var x = {var_x}, var y = {var_y}')
    seconds_needed += 1
    bots = [Robot(b.position + b.speed, b.speed) for b in bots]
print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {seconds_needed}')

# lol this actually worked, i was thinking of printing out all images
# and the name would be the seconds elapsed and then going through them
# in the folder to find the tree lol
# just for fun i actually printed them all from 0 to 9999
# seconds_needed: int = 0
# f = open('search_for_trees.txt', 'a')
# for _ in range(10000):
#     print(f'[Elapsed seconds: {seconds_needed}]\n')
#     f.write(f'[Elapsed seconds: {seconds_needed}]\n')
#     f.write(pretty_print(bots))
#     f.write('\n')
#     seconds_needed += 1
#     bots = [Robot(b.position + b.speed, b.speed) for b in bots]
# f.close()
# it's a 100MB file lol, and finding it it's still difficult
