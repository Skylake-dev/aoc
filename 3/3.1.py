from common import priority

data = open('./input')
priority_per_line = []

for line in data:
    line = line.strip()
    length = len(line)
    assert (length % 2) == 0
    first_compartment = sorted(line[:(length // 2)])
    second_compartment = sorted(line[(length // 2):])

    i = 0
    j = 0

    while (i < (length // 2)) or (j < (length // 2)):
        if first_compartment[i] == second_compartment[j]:
            priority_per_line.append(priority[first_compartment[i]])
            break
        elif first_compartment[i] < second_compartment[j]:
            i += 1
        else:
            j += 1

print(f'total priority = {sum(priority_per_line)}')

data.close()