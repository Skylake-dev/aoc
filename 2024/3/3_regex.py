import re
from functools import reduce

with open('./input') as f:
    input = f.readlines()

# join all lines
s: str = ''.join(input)

###############
# utils
###############


def do_mul(mul: str) -> int:
    """Takes a mul instruction in the format mul(op1,op2)
    and returns the result of the multiplication.

    Parameters
        mul: string containing the mul

    Returns
        the result of op1,op2
    """
    operands = re.findall(r'\d+', mul)
    return reduce(lambda x, y: x*y, map(int, operands))


###############
# part 1
###############

result: int = 0
# for part 1 i just need mul
part_1_regex = r"mul\([0-9]+,[0-9]+\)"
matches = re.findall(part_1_regex, s)
# simply add up the results
for m in matches:
    result += do_mul(m)

print(f'part 1 {result}')

###############
# part 1
###############

result: int = 0
# at the start operations are enabled
do: bool = True
# in part 2 i also need flags
part_2_regex = r"do\(\)|don't\(\)|mul\([0-9]+,[0-9]+\)"
# findall returns matches in the order that they were found
matches = re.findall(part_2_regex, s)
for m in matches:
    if m == 'do()':
        do = True
    elif m == 'don\'t()':
        do = False
    else:
        # only do the mul if the flag is active
        if do:
            result += do_mul(m)


print(f'part 2 {result}')
