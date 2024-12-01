# divide by 3 --> floor ---> sutract 2
file = open('./2019/input')
total = []
total_adj =[]
data = file.readlines()

# part 1
for line in data:
    fuel = (int(line) // 3) - 2
    total.append(fuel)

print(f'total = {sum(total)}')

# part 2
for line in data:
    fuel = 0
    added = (int(line) // 3) - 2
    while added > 0:
        fuel += added
        added = (added // 3) - 2
    total_adj.append(fuel)

print(f'total adjusted = {sum(total_adj)}')