import re

def parse_stacks(lines: list, num_stacks) -> list:
    stacks = [[] for i in range(num_stacks)]
    for index, stack in enumerate(stacks):
        for line in lines:
            char = line[1 + 4*index]
            if char != ' ':
                stack.append(char)
    return stacks

def parse_move(line: str) -> list:
    return re.findall(r'\d+', line)

def do_move(stacks: list, quantity: int, start: int, dest: int) -> None:
    quantity = int(quantity)
    start = int(start) - 1
    dest = int(dest) - 1
    while quantity > 0:
        stacks[dest].insert(0, stacks[start].pop(0))
        quantity -= 1

def do_n_move(stacks: list, quantity: int, start: int, dest: int) -> None:
    quantity = int(quantity)
    start = int(start) - 1
    dest = int(dest) - 1
    to_move = stacks[start][0:quantity]
    stacks[start] = stacks[start][quantity:]
    stacks[dest] = to_move + stacks[dest]
    print(to_move)
    print(stacks[start])
    print(stacks[dest])

def get_answer(stacks: list) -> str:
    answer = ''
    for stack in stacks:
        answer += stack[0]
    return answer