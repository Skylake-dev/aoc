from time import time

with open('../inputs/22.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

# list all the initial secrest, one on each line
secrets: list[int] = [int(l.strip()) for l in input]

###############
# utils
###############


def _mix(secret: int, value: int) -> int:
    return secret ^ value


def _prune(value: int) -> int:
    return value % 16777216


def evolve(secret: int) -> int:
    """Function to compute the next secret number, given its predecessor.

    Parameters
        secret: the predecessor number

    Returns
        the next secret according to the pseudorandom function
    """
    # step 1
    result = secret * 64
    result = _prune(_mix(secret, result))
    # step 2
    result = _prune(_mix(result, result // 32))
    # step 3
    result = _prune(_mix(result, result * 2048))
    return result


def evolve_n_times(secret: int, times: int) -> int:
    """Function to compute the `times` iterations of the evolution
    process.

    Parameters
        secret: the predecessor number
        times: the number of times to evolve

    Returns
        the `times` next secret
    """
    for _ in range(times):
        secret = evolve(secret)
    return secret

###############
# part 1
###############


# track time
begin: float = time()
sum = 0
for num in secrets:
    sum += evolve_n_times(num, 2000)
print(f'[part 1] time: {(time()-begin):.4f}s')
print(f'part 1: {sum}')

###############
# part 2
###############

# track time
begin: float = time()

print(f'[part 2] time: {(time()-begin):.4f}s')
print(f'part 2: {0}')
