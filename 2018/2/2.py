from functools import reduce

with open('./input') as data:
    input = data.readlines()

# remove \n
input = [el.strip() for el in input]

###############
# part 1
###############

double_count = 0
triple_count = 0

for line in input:
    seen: dict[str, int] = {}
    for char in line:
        if char in seen:
            seen[char] += 1
        else:
            seen[char] = 1
    if 2 in seen.values():
        double_count += 1
    if 3 in seen.values():
        triple_count += 1

print(f'part 1: {double_count*triple_count}')

###############
# part 2
###############

# number of different characters in same len strings
def distance(line1, line2) -> int:
    distance = 0
    for i in range(len(line1)):
        if line1[i] != line2[i]:
            distance += 1
    return distance

# find any two strings that differ only by 1 char
def find_lines() -> tuple[str, str]:
    for i, line1 in enumerate(input):
        for line2 in input[i:]:
            if distance(line1, line2) == 1:
                return line1, line2
    return '', ''

line1, line2 = find_lines()
out = ''
for i in range(len(line1)):
    if line1[i] == line2[i]:
        out += line1[i]

print(f'part 2: {out}')