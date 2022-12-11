import re
from typing import List
from common import (
    Monkey,
    parse_monkey_params
)

data = open('./input')

monkeys: List[Monkey] = []

line = data.readline().strip()
while(line != ''):
    if line.startswith('Monkey'):
        monkey = Monkey(int(re.findall(r'\d+', line)[0]))
        monkeys.append(monkey)
        parse_monkey_params(data, monkey)
    line = data.readline()
data.close()

rounds = 20

for round in range(rounds):
    for monkey in monkeys:
        for idx, item in enumerate(monkey.items):
            monkey.curr_item = item
            monkey.inspect()
            monkey.bored()
            outcome = monkey.test()
            if outcome:
                monkeys[monkey.next_if_true].add_item(item)
            else:
                monkeys[monkey.next_if_false].add_item(item)
        # at the end of its turn monkey has thrown all items
        monkey.items = []

inspections = sorted([m.inspections_count for m in monkeys], reverse=True)
print(
    f'Monkey business = {inspections[0]*inspections[1]} ({inspections[0]}*{inspections[1]})')
