from functools import reduce

with open('./input') as data:
    input = data.readlines()

# parse as int
input = [int(el) for el in input]

###############
# part 1
###############

print(f'part 1: {reduce(lambda x,y: x+y, input)}')

###############
# part 2
###############

# actually need to simulate all steps to keep track of all
# the values that are reached
current_frequency = 0
seen = set()
seen.add(current_frequency)
found = False

while not found:
    for change in input:
        current_frequency += change
        if current_frequency in seen:
            # i found the repeated value
            found = True
            break
        seen.add(current_frequency)

print(f'part 2: {current_frequency}')