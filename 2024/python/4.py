from typing import Callable, Iterable

with open('../inputs/4.txt') as data:
    lines: list[str] = data.readlines()

# remove newlines
lines = [l.strip() for l in lines]

###############
# utils
###############

# lines is always treated as a matrix of characters
# these functions return different views on the same lines
# horizontal is the input as is
# the matrix is square


def horizontal(lines: list[str]) -> list[str]:
    """Return input as is, just helper function."""
    return lines


def backward_horizontal(lines: list[str]) -> list[str]:
    """Reverse all rows in the input."""
    return [row[::-1] for row in lines]


def vertical(lines: list[str]) -> list[str]:
    """Return the list by columns."""
    return [''.join(el) for el in zip(*lines)]


def backwards_vertical(lines: list[str]) -> list[str]:
    """Return the list by columns starting from the bottom."""
    return [col[::-1] for col in vertical(lines)]


def _diag_ltr_idxs(lines: list[str], backwards=False) -> list[list[tuple[int, int]]]:
    # helper to compute indexes of left to right diags
    # nxn matrix means 2n-1 diagonals. for each diagonal the
    # difference of indexes is constant (consider y-x because
    # i found it easier to think about) e.g.
    # [(3,0)] -> y-x=-3
    # [(2,0),(3,1)] -> y-x=-2
    result: list[list[tuple[int, int]]] = []
    n: int = len(lines[0])
    max_idx: int = n - 1
    for diff in range(-max_idx, max_idx+1):
        # list all pairs with that diff
        diag: list[tuple[int, int]] = []
        # count is the number of elements in this diagonal
        count = n - (abs(diff))
        for i in reversed(range(count)):
            x = min(max_idx-i-diff, max_idx-i)
            y = x+diff  # since y-x=diff y is determined like this
            diag.append((x, y))
        if backwards:
            result.append(list(reversed(diag)))
        else:
            result.append(diag)
    return result


def _diag_rtl_idxs(lines: list[str], backwards=False) -> list[list[tuple[int, int]]]:
    # helper to compute indexes of right to left diags
    # same considerations as _diag_ltr_idxs applies
    # just use a different indexing. The condition this time
    # is that the sum of the indexes is constant.
    result: list[list[tuple[int, int]]] = []
    n: int = len(lines[0])
    max_idx: int = n - 1
    for sum in range(2*max_idx + 1):
        # list all pairs with that sum
        diag: list[tuple[int, int]] = []
        # count is the number of elements in this diagonal
        count = sum + 1 if sum < n else 2*max_idx-sum + 1
        for i in range(count):
            x = i if sum < n else i+(sum-n)+1
            y = sum-x  # since x+y=sum y is determined like this
            diag.append((x, y))
        if backwards:
            result.append(list(reversed(diag)))
        else:
            result.append(diag)
    return result


def diagonal_left_to_right(lines: list[str]) -> list[str]:
    """Return the list by diagonals in the input in left
    to right order, bottom left to top right.
    Of course elements will not have the same length.
    """
    result: list[str] = []
    # use the helper function to compute indexes
    for diag in _diag_ltr_idxs(lines):
        text: str = ''
        for position in diag:
            text += lines[position[0]][position[1]]
        result.append(text)
    return result


def backwards_diagonal_left_to_right(lines: list[str]) -> list[str]:
    """Return the list by diagonals from left to right in reverse."""
    return [diag[::-1] for diag in diagonal_left_to_right(lines)]


def diagonal_right_to_left(lines: list[str]) -> list[str]:
    """Return the list by diagonals in the input in right
    to left order, top left to bottom right.
    Of course elements will not have the same length.
    """
    # same considerations as diagonal_left_to_right applies
    # just use a different indexing. The condition this time
    # is that the sum of the indexes is constant
    result: list[str] = []
    # use the helper function to compute indexes
    for diag in _diag_rtl_idxs(lines):
        text: str = ''
        for position in diag:
            text += lines[position[0]][position[1]]
        result.append(text)
    return result


def backwards_diagonal_right_to_left(lines: list[str]) -> list[str]:
    """Return the list by diagonals from right to left in reverse."""
    return [diag[::-1] for diag in diagonal_right_to_left(lines)]


# all the possible views
views: list[Callable[[list[str]], list[str]]] = [
    horizontal,
    backward_horizontal,
    vertical,
    backwards_vertical,
    diagonal_left_to_right,
    backwards_diagonal_left_to_right,
    diagonal_right_to_left,
    backwards_diagonal_right_to_left
]


def find_all(substring: str, s: str) -> list[int]:
    """Returns the list of all the starting indexes of the
    substring in the s string.

    Parameters
        substring: the substring to find
        s: the target string

    Returns
        list of starting positions of all the substring occurrences.
        The list is empty if no match is found
    """
    result: list[int] = []
    start = 0
    while True:
        start = s.find(substring, start)
        if start == -1:
            # no match, return what i found so far
            # (can be empty)
            return result
        result.append(start)
        start += len(substring)  # since the string cannot overlap i skip over


# step to take from start of match to the 'A' in MAS
steps: dict[Callable[[list[str]], list[str]], tuple[int, int]] = {
    horizontal: (0, 1),
    backward_horizontal: (0, -1),
    vertical: (1, 0),
    backwards_vertical: (-1, 0),
    diagonal_left_to_right: (1, 1),
    backwards_diagonal_left_to_right: (-1, -1),
    diagonal_right_to_left: (1, -1),
    backwards_diagonal_right_to_left: (-1, 1)
}


def add_step(start: tuple[int, int], view: Callable[[list[str]], list[str]]) -> tuple[int, int]:
    """Return the position for the 'A' in match given the starting
    position and the view
    """
    return (start[0]+steps[view][0], start[1]+steps[view][1])


###############
# part 1
###############


TARGET: str = 'XMAS'
# count substring in all possible directions
# i just use the helpers to get the right orders
result: int = 0
for view in views:
    # keep track of the occurrences for each view
    old_res = result
    for line in view(lines):
        result += line.count(TARGET)
    print(f'view {view.__name__}: {result-old_res} occurrences')


print(f'part 1: {result}')

###############
# part 2
###############

TARGET: str = 'MAS'
# need to keep track of the positions of all the matches
# and see if they overlap. Since i know the ordering
# of all the views i can just enumerate all the positions
# the general idea is:
# - find the positions of target in all diagonals
# - compute the position of the 'A'
# - if 2 matches have the same position for the 'A' then they
#   produce an X-MAS so i count that
result: int = 0
# keep track of the 'A' that i saw in a set, if a position
# is in a match and was already seen then it's an X-MAS
a_positions: set[tuple[int, int]] = set()
# possible views and indexes
cases: dict[Callable[[list[str]], list[str]], Iterable[tuple[str, list[tuple[int, int]]]]] = {
    diagonal_left_to_right: zip(diagonal_left_to_right(lines), _diag_ltr_idxs(lines)),
    backwards_diagonal_left_to_right: zip(backwards_diagonal_left_to_right(lines),
                                          _diag_ltr_idxs(lines, backwards=True)),
    diagonal_right_to_left: zip(diagonal_right_to_left(lines), _diag_rtl_idxs(lines)),
    backwards_diagonal_right_to_left: zip(backwards_diagonal_right_to_left(lines),
                                          _diag_rtl_idxs(lines, backwards=True)),
}

for view, case in cases.items():
    for diag, idxs in case:
        # match each line
        matched_indexes = find_all(TARGET, diag)
        # get the position of the 'A' in the current line
        line_positions = [add_step(idxs[m], view) for m in matched_indexes]
        # check if i already saw that 'A'
        for a in line_positions:
            if a in a_positions:
                # found a match, count
                result += 1
            else:
                # otherwise keep track
                a_positions.add(a)

print(f'part 2: {result}')
