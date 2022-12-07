from common import (
    root,
    process_command,
    process_output,
    walk_tree
)

data = open('./input')

cwd = root

for line in data:
    if line.startswith('$'):
        cwd = process_command(line, cwd)
    else:
        process_output(line, cwd)

# part 1
space_to_free = 100000
total_size = 0  # note: will count files twice by design

for dir in walk_tree(root):
    if dir.size <= space_to_free:
        total_size += dir.size

print(f'total size = {total_size}')

# part 2
total_space = 70000000
required_space = 30000000
unused_space = total_space - root.size
space_to_free = required_space - unused_space

candidate_dir = root

for dir in walk_tree(root):
    if dir.size >= space_to_free:
        if dir.size < candidate_dir.size:
            candidate_dir = dir

print(
    f'directory to delete is {candidate_dir.name} of size {candidate_dir.size}')

data.close()
