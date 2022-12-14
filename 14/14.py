from common import Cave

with open('./input') as data:
    cave = Cave(data)

# part 1
total_sand_fallen = 0

while not cave.max_depth_reached:
    cave.sand_fall(cave.sand_spawn_point)
    total_sand_fallen += 1

print(f'(part1) total sand fallen = {total_sand_fallen - 1}')

# part 2
cave.remove_sand()
cave.add_bottom()
total_sand_fallen = 0

while not cave.spawn_reached:
    cave.sand_fall(cave.sand_spawn_point)
    total_sand_fallen += 1

print(f'(part2) total sand fallen = {total_sand_fallen}')
