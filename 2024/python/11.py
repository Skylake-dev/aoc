from math import log10, floor
from time import time
from functools import cache
from collections import Counter

with open('../inputs/11.txt') as data:
    # it's a single line
    input = data.readline().strip()

###############
# input parsing
###############

# get the list of stones
raw_stones: list[int] = list(map(int, input.split(' ')))
# this is very bad for a high number of blinks
# need to use a more efficient structure
# since the list will become huge
# (12 million elements at step 38, roughly +60% size per iteration)
# the order of the stones doesn't matter so i can just
# track stones in a dictionary stone: count
# hopefully we have a lot of repeating numbers
stones = Counter(raw_stones)

###############
# utils
###############


@cache
def apply_rules(stone: int) -> list[int]:
    """Applies the rules to the current stone and returns
    a list containing the resulting stones.

    Parameters
        stone: the current stone

    Returns
        a list with 1 or 2 stones, depending on the rules
        applied, that will replace the current stone
    """
    # if it's 0, replace it with a 1
    if stone == 0:
        return [1]
    # if it has an even number of digits,
    # split in two and remove leading zeros
    digits: int = floor(log10(stone) + 1)
    if digits % 2 == 0:
        # i should not use string conversion because it's slow
        # i can do an integer division for the upper part and
        # a modulus for the lower using the number of digits
        power = 10 ** (digits//2)
        return [stone // power, stone % power]
    # none of the previous rules apply, multiply
    # by 2024 and return it
    return [stone*2024]


def blink(stones: dict[int, int]) -> dict[int, int]:
    """Apply rules on all stones and returns the new set of stones."""
    # avoid updating during iteration, just save the result in a new
    # dictionary
    new_stones: dict[int, int] = {}
    for i, (stone, count) in enumerate(stones.items()):
        # apply rule to current stone
        res = apply_rules(stone)
        # add the resulting stones to the total
        # taking into account that this does `count` operations
        for s in res:
            if s in new_stones:
                new_stones[s] += count
            else:
                new_stones[s] = count
    return new_stones

###############
# part 1
###############


# track time
begin: float = time()
# apply rules to all the stones for 25 blinks
N_BLINKS = 25
stones1 = stones  # use a different variable for p1 to keep the original stones for p2
for _ in range(N_BLINKS):
    stones1 = blink(stones1)
print(f'[part 1] time: {(time()-begin):.4f}s')
print(f'part 1: {sum(stones1.values())}')

###############
# part 2
###############

# track time
begin: float = time()
# apply rules to all the stones for 75 blinks
N_BLINKS = 75
for _ in range(N_BLINKS):
    stones = blink(stones)
print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {sum(stones.values())}')
