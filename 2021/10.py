file = open('./2021/input')
data = file.readlines()


open_par = ('(', '[', '{', '<')

matching = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}

# part 1
points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

corrupt_score_per_line = []
total_score = 0

for line in data:
    syntax_tree = []
    corrupt_score_per_line.append(0)
    for char in line:
        if char == '\n':
            break
        if char in open_par:
            syntax_tree.append(char)
        elif char in matching:
            if syntax_tree[-1] == matching[char]:
                syntax_tree.pop(-1)
            else:
                print(f'found {char} but matching parenthesis was {syntax_tree[-1]}')
                corrupt_score_per_line[-1] = points[char]
                break
        
print(f'total corrupted score = {sum(corrupt_score_per_line)}')

# part 2
incomplete_lines = [data[i] for i in range(len(corrupt_score_per_line)) if corrupt_score_per_line[i] == 0]
print(len(incomplete_lines))

# i have open par in my stack, i match against those
points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def compute_score(chars):
    score = 0
    for char in reversed(chars):  # need to close in reverse order
        score *= 5
        score += points[char]
    return score

incomplete_score_per_line = []

# note: can be optimized if i save the incomplete syntax trees from before
for line in incomplete_lines:
    syntax_tree = []
    for char in line:
        if char == '\n':
            break
        if char in open_par:
            syntax_tree.append(char)
        elif char in matching:
            if syntax_tree[-1] == matching[char]:
                syntax_tree.pop(-1)
    incomplete_score_per_line.append(compute_score(syntax_tree))

incomplete_score_per_line.sort()
print(f'middle score = {incomplete_score_per_line[len(incomplete_score_per_line) // 2]}')