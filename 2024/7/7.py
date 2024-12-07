from itertools import permutations
from functools import reduce
from time import time

with open('./input') as data:
    input = data.readlines()

###############
# input parsing
###############

# save the target result and the operands
targets: list[int] = []
operands_list: list[list[int]] = []
for line in input:
    res, ops = line.split(':')
    targets.append(int(res))
    operands_list.append([int(op) for op in ops.strip().split(' ')])

###############
# utils
###############


def possible_permutations_part1(n: int) -> set[tuple[str, ...]]:
    """Provide a list with all the permutations for the operators
    given an `n` number of operands. The result is given in a list
    of tuples containing all the permutations, e.g.
    for n=3 -> [(+, +), (*, +), (+, *), (*, *)]
    (3 operands means 2 operations -> 2^2 possibilities)

    Parameters
        n: number of operands

    Returns
        a list with all the possible operand sequences
    """
    combs: set[tuple[str, ...]] = set()
    # all the permutations of the strings
    # containing the operator count, e.g for n=5
    # ++++ -> *+++ -> **++ -> ***+ -> ****
    # the range goes from 0 to n-1 so it's perfect
    for muls in range(n):
        ops: str = (n-muls-1)*'+' + muls*'*'
        # set returns only the unique permutations
        c: set[tuple[str, ...]] = set(permutations(ops))
        combs = combs.union(c)
    return combs


def possible_permutations_part2(n: int) -> set[tuple[str, ...]]:
    """Provide a list with all the permutations for the operators
    given an `n` number of operands. The result is given in a list
    of tuples containing just the permutations with the new operator, e.g.
    for n=3 -> [(+, +), (*, +), (+, *), (*, *)
                (||, +), (+, ||), (||, *), (*, ||) (||, ||)]
    (3 operands means 2 operations -> 3^2 possibilities)
    These are all possible combinations but the function will only
    return the ones with the new operator, that in this case are
        [(||, +), (+, ||), (||, *), (*, ||) (||, ||)]]
    Also for practical reasons the || is shortened to |, so the result
    will be
        [(|, +), (+, |), (|, *), (*, |) (|, |)]]

    Parameters
        n: number of operands

    Returns
        a list with all the possible operand sequences
    """
    combs: set[tuple[str, ...]] = set()
    # add || one at a time and produce permutations
    ops: str = ''
    for concat in range(1, n):
        ops = concat*'|'
        # produce the rest of the symbols in all possible configurations
        for muls in range(n-concat):
            complete_ops = ops + (n-concat-muls-1)*'+' + muls*'*'
            # set returns only the unique permutations
            c: set[tuple[str, ...]] = set(permutations(complete_ops))
            combs = combs.union(c)
    return combs


# compute the max and min for the length of permutations
lengths = [len(op) for op in operands_list]
min_len = min(lengths)
max_len = max(lengths)

###############
# part 1
###############

# produce the permutations only once for all the possible operand length
# precompute the results so that i don't have to do it over and over again
print('[part 1]producing perms')
begin: float = time()
all_perms_part1: dict[int, set[tuple[str, ...]]] = {}
for i in range(min_len, max_len+1):
    all_perms_part1[i] = possible_permutations_part1(i)
print(f'[part 1]done in {(time()-begin):.3f}s')

print('[part 1]computing result')
begin: float = time()
result: int = 0
# keep track of correct sequences so i don't need to redo it
# (i counted that they are a bit more than 1/3)
correct_operations: list[bool] = len(targets)*[False]
# idk just bruteforce the operators
for i, (target, operands) in enumerate(zip(targets, operands_list)):
    # get all possible sequences of operands
    perms = all_perms_part1[len(operands)]
    # small optimization, if i cannot reach the target by multiplying
    # all the operands then i can skip this (i don't know if it is better
    # or not lol)
    if reduce(lambda x, y: x*y, operands) < target:
        continue
    # try them all, if i can fit one then i count this
    # value in the solution
    for operators_sequence in perms:
        # keep track of current value
        partial_res: int = operands[0]
        for operator, operand in zip(operators_sequence, operands[1:]):
            if operator == '*':
                partial_res *= operand
            elif operator == '+':
                partial_res += operand
            if partial_res > target:
                # i don't know if it's worth it but i could exit
                # early if i go over the target
                break
        # check if the target is reached
        if partial_res == target:
            # count it and break (i don't care if there are multiple)
            result += partial_res
            # keep track of correct ones
            correct_operations[i] = True
            break
print(f'[part 1]done in {(time()-begin):.3f}s')
print(f'part 1: {result}')

###############
# part 2
###############

# also precompute here, will be much slower (3^n instead of 2^n)
print('[part 2]producing perms')
begin: float = time()
all_perms_part2: dict[int, set[tuple[str, ...]]] = {}
for i in range(min_len, max_len+1):
    # join with the previous ones
    all_perms_part2[i] = all_perms_part1[i].union(
        possible_permutations_part2(i))
print(f'[part 2]done in {(time()-begin):.3f}s')

# same logic as part 1 but i can concatenate any two numbers
# before checking and i only need permutations of the operator
# one item shorter e.g.
# [1, 2, 3] -> only produce one operand and try all concatenations
# 12 + 3, 12 * 3, 1 + 23, 1 * 23
# only check the incorrect ones, and do not reset result since
# the answer also keeps the ones from before
print('[part 2]computing result')
begin: float = time()
for correct, target, operands in zip(correct_operations, targets, operands_list):
    if correct:
        # i already computed those in part 1
        continue
    # get the permutation for one fewer element than operands
    # counts since i will join two of them
    perms = all_perms_part2[len(operands)]
    for operators_sequence in perms:
        # keep track of current value
        partial_res: int = operands[0]
        for operator, operand in zip(operators_sequence, operands[1:]):
            if operator == '*':
                partial_res *= operand
            elif operator == '+':
                partial_res += operand
            elif operator == '|':
                partial_res = int(str(partial_res)+str(operand))
            if partial_res > target:
                # i don't know if it's worth it but i could exit
                # early if i go over the target
                break
        # check if the target is reached
        if partial_res == target:
            # count it and break (i don't care if there are multiple)
            result += partial_res
            break

print(f'[part 2]done in {(time()-begin):.3f}s')
print(f'part 2: {result}')
