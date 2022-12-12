from common import (
    Heatmap,
    shortest_path
)
with open('./input') as data:
    heatmap = Heatmap(data)

# part 1
path = shortest_path(heatmap, heatmap.start, heatmap.end)
print(f'shortest path is {len(path) - 1} steps')

# part 2
min_path = 100000
for cell in heatmap.iterate():
    if cell.height == 0:
        heatmap.reset_visits()
        path = shortest_path(heatmap, cell, heatmap.end)
        if not path == [] and ((len(path) - 1) < min_path):
            min_path = len(path) - 1
print(f'shortest path from elevation 0 is {min_path} steps')
