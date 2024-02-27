file = open('./input')
elf = 0
elves_cal = [0]
for line in file.readlines():
    if line != '\n':
        elves_cal[elf] += int(line)
    else:
        elves_cal.append(0)
        elf += 1

print(f'there are {len(elves_cal)} in total')
elves_cal.sort(reverse=True)
print(f'Top 3: {elves_cal[0]}, {elves_cal[1]}, {elves_cal[2]}')
print(f'total = {elves_cal[0]+elves_cal[1]+elves_cal[2]}')