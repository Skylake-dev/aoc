import re

with open('./input') as data:
    input = data.readlines()

integer = r'[0-9]+'
integer = re.compile(integer)

###############
# input parsing
###############

reports: list[list[int]] = []
for line in input:
    # get all integers in a list and append to reports
    reports.append(list(map(int, re.findall(integer, line))))

###############
# utils
###############


def condition(i1: int, i2: int, is_ascending: bool) -> bool:
    """Check the condition of increment for each pair of elements
    depending on the direction

    Parameters
        i1: first input in position i
        i2: second input in position i+1
        is_ascending: True if ascending list, False if descending

    Returns
        True if the condition is satisfied, i.e. the increment/decrement
        is in [1,3], False otherwise
    """
    if is_ascending:
        if 1 <= i2 - i1 <= 3:
            return True
    else:
        if 1 <= i1 - i2 <= 3:
            return True
    return False


def check_safety(report: list[int]) -> bool:
    """Check whether a report is safe or not. A report is safe when
    - all elements are either in ascending or descending order
    - the step from one element to the next is at least 1 and at most 3
        included

    Parameters
        report: the current report

    Returns
        True if it's safe, False otherwise
    """
    # check if should be ascending or descending
    # True if ascending, False if descending
    is_ascending: bool = report[0] < report[1]
    for i in range(len(report) - 1):
        # then check that increments/decrements between elements are in [1,3]
        if not condition(report[i], report[i+1], is_ascending):
            return False
    # no violation found
    return True

###############
# part 1
###############


print(f'part 1: {len(list(filter(check_safety, reports)))}')

###############
# part 2
###############

# keep track of safe
safe_count: int = 0

# bruteforce all combinations, if a filter is not safe
# after removing any element then it's discarded
# i can do this since reports are short (<10 values)
for n, report in enumerate(reports):
    # if it's already safe, skip
    if check_safety(report):
        safe_count += 1
        continue
    # otherwise try removing all elements one by one
    # and check
    for i in range(len(report)):
        el = report.pop(i)
        if check_safety(report):
            # removing this element makes it safe
            print(f'[{n}]safe after removing {el} (index {i})')
            safe_count += 1
            break
        # otherwise, place the element back for next iteration
        report.insert(i, el)

print(f'part 2: {safe_count}')
