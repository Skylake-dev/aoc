from common import priority

data = open('./input')
priority_per_line = []

lines = data.readlines()
groups = [lines[3*i : 3*(i+1)] for i in range((len(lines) // 3))]

for group in groups:
    first = sorted(group[0].strip())
    second = sorted(group[1].strip())
    third = sorted(group[2].strip())

    i = 0
    j = 0
    k = 0

    while (i < len(first)) or (j < len(second)) or (k < len(third)):
        if first[i] == second[j]:
            if second[j] == third[k]:
                priority_per_line.append(priority[first[i]])
                break
            elif second[j] < third[k]:
                i += 1
                j += 1
            else:
                k += 1
        if first[i] < second[j]:
            i += 1
            if third[k] < second[j]:
                k += 1
            elif third[k] > second[j]:
                j += 1
        if first[i] > second[j]:
            j += 1
            if third[k] < first[i]:
                k += 1
            elif third[k] > first[i]:
                i += 1

print(f'total priority = {sum(priority_per_line)}')

data.close()