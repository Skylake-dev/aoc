import re

with open('./input') as data:
    input = data.readlines()

claim = r'#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)'
claim = re.compile(claim)

parsed_input = []
# parse line
for line in input:
    id, start_x, start_y, width, height = claim.match(line).group(1, 2, 3, 4, 5)
    parsed_input.append((int(id), int(start_x), int(start_y), int(width), int(height)))

###############
# part 1
###############

# for each point count occupants
occupation_count: dict[tuple[int,int], int] = {}

for line in parsed_input:
    id, start_x, start_y, width, height = line
    # zero indexed so it's offset by 1
    for x in range(start_x, start_x + width):
        for y in range(start_y, start_y + height):
            if (x, y) in occupation_count:
                occupation_count[(x,y)] += 1
            else:
                occupation_count[(x,y)] = 1

print(f'part 1: {sum([1 for cell in occupation_count if occupation_count[cell] > 1])}')

###############
# part 2
###############

# go over the list again and find the one block without
# any overlap (occupation = 1 for all area)
# i can exit immediately since there is exactly one
for line in parsed_input:
    id, start_x, start_y, width, height = line
    overlap = False
    for x in range(start_x, start_x + width):
        if overlap:
            break
        for y in range(start_y, start_y + height):
            if occupation_count[(x,y)] > 1:
                overlap = True
                break
    if not overlap:
        break

print(f'part 2: {id}')