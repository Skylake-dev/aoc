import re
from collections import Counter

with open('./input') as data:
    input = data.readlines()

numbers = r'([0-9]+)   ([0-9]+)'
numbers = re.compile(numbers)

###############
# input parsing
###############

left: list[int] = []
right: list[int] = []

for line in input:
    m = numbers.match(line)
    assert m is not None
    left_number, right_number = m.group(1, 2)
    left.append(int(left_number))
    right.append(int(right_number))

left.sort()
right.sort()

###############
# part 1
###############

# sum of the absolute difference between each element
# in the sorted lists
result = sum([abs(l-r) for l, r in zip(left, right)])
print(f'part 1: {result}')

###############
# part 2
###############

# count all occurrences in right list
counts = Counter(right)
# for each element in left list, add
# the count value of the right if present
similarity_score = 0
for num in left:
    if num in counts:
        similarity_score += num*counts[num]

print(f'part 2: {similarity_score}')