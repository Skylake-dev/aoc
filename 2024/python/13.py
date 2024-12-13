import re

from time import time
from collections import namedtuple
from dataclasses import dataclass

with open('../inputs/13.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

Vector = namedtuple('Vector', ['x', 'y'])


@dataclass
class Machine:
    """Store the two button increments and the location of the prize"""
    a: Vector
    b: Vector
    prize: Vector


# keep a list of all the machines
machines: list[Machine] = []

# regex to parse integers from the line
integer = r'[0-9]+'
integer = re.compile(integer)

# read lines in blocks of 4, one for each machine
for i in range(0, len(input), 4):
    # a button movement
    a = Vector(*list(map(int, re.findall(integer, input[i]))))
    # b button movement
    b = Vector(*list(map(int, re.findall(integer, input[i+1]))))
    # prize location
    prize = Vector(*list(map(int, re.findall(integer, input[i+2]))))
    # line i+3 is a blank
    # add machine to the list
    m: Machine = Machine(a=a, b=b, prize=prize)
    machines.append(m)


###############
# utils
###############

# note that we basically want to solve a linear system
# to find possible solutions (then i need to figure out how to minimize it)
# e.g. this machine
# Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
# can be modeled by the system of equations
# 94A + 22B = 8400
# 34A + 67B = 5400
# where A and B are the number of button presses
# then with some linear algebra i can check how many solutions there are
# note: i checked on my input and all solutions are unique, so i can just
# compute it by solving the linear equation
def _det(a1, a2, b1, b2) -> int:
    return a1*b2 - b1*a2


def solve(m: Machine) -> tuple[float, float]:
    """Given a machine produce the raw solution. Basically
    solve the linear system associated to it.

    Parameters
        m: the current machine with buttons and target prize location

    Returns
        a Vector containing the solution
    """
    # use helper variables to represent the matrix
    # associated to the linear system
    #  | a1   b1 | | A |   | c1 |
    #  |         |*|   |   |    |
    #  | a2   b2 | | B |   | c2 |
    a1 = m.a.x
    a2 = m.a.y
    b1 = m.b.x
    b2 = m.b.y
    c1 = m.prize.x
    c2 = m.prize.y
    # sanity check, but i already checked my whole input,
    # that the determinant is not 0 (unique solution)
    M = _det(a1, a2, b1, b2)
    assert M != 0
    # use cramer method
    a_presses = _det(c1, c2, b1, b2) / M
    b_presses = _det(a1, a2, c1, c2) / M
    return (a_presses, b_presses)


###############
# part 1
###############

# track time
begin: float = time()
# cost is 3 for each A button press and 1 for each B button press
total_cost: int = 0
for m in machines:
    a_presses, b_presses = solve(m)
    # check that they are integer, in python the modulus operator works
    if a_presses % 1 == 0.0 and b_presses % 1 == 0.0:
        total_cost += int(a_presses)*3 + int(b_presses)
# cannot use the usual format since it's too fast, use us
# time is probably too imprecise for this
print(f'[part 1] time: {(time()-begin)*1000000:.4f}us')
print(f'part 1: {total_cost}')

###############
# part 2
###############

# track time
begin: float = time()
total_cost: int = 0
# same as part 1, just adjust coords by offset
offset = 10000000000000
for m in machines:
    m.prize = Vector(m.prize.x+offset, m.prize.y+offset)
    a_presses, b_presses = solve(m)
    # check that they are integer, in python the modulus operator works
    if a_presses % 1 == 0.0 and b_presses % 1 == 0.0:
        total_cost += int(a_presses)*3 + int(b_presses)
print(f'[part 2] time: {(time()-begin)*1000000:.4f}us')
print(f'part 2: {total_cost}')
