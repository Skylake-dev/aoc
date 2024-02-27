from common import (
    parse_stacks,
    parse_move,
    do_n_move,
    get_answer
)

data = open('./input')

stack_lines = []
stacks = []  # one list per stack, stack[0] is the top

for line in data:
    if line == '\n':
        continue
    if line.startswith('['):       # stacks
        stack_lines.append(line)
    elif line.strip().startswith('1'):
        num_stacks = [int(num) for num in line.split()][-1]  # the last number is the number of stacks
        stacks = parse_stacks(stack_lines, num_stacks)
    else:
        quantity, start, dest = parse_move(line.strip())
        do_n_move(stacks, quantity, start, dest)

print(f'answer = {get_answer(stacks)}')


data.close()