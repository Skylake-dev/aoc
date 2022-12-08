from common import (
    Tree,
    Forest,
    compute_visibility
)

data = open('./input')

forest = Forest()

for line in data:
    forest.add_row([Tree(int(height)) for height in line.strip()])

# part 1
for column in forest.cols_top_to_bottom():
    compute_visibility(column)
for column in forest.cols_bottom_to_top():
    compute_visibility(column)
for row in forest.rows_left_to_right():
    compute_visibility(row)
for row in forest.rows_right_to_left():
    compute_visibility(row)

print(f'Total visible trees: {forest.count_visible()}')

# part 2
rows, columns = forest.dimensions()
max_score = 0
for i in range(rows):
    for j in range(columns):
        row = forest.get_row(i)
        col = forest.get_col(j)
        tree = forest.get_tree(i, j)
        left_score = right_score = up_score = down_score = 0
        for t in reversed(row[:j]):
            left_score += 1
            if t.height >= tree.height:
                break
        for t in row[j+1:]:
            right_score += 1
            if t.height >= tree.height:
                break
        for t in reversed(col[:i]):
            up_score += 1
            if t.height >= tree.height:
                break
        for t in col[i+1:]:
            down_score += 1
            if t.height >= tree.height:
                break
        tree.scenic_score = left_score * right_score * up_score * down_score
        if tree.scenic_score > max_score:
            max_score = tree.scenic_score

print(f'max scenic score = {max_score}')

data.close()
