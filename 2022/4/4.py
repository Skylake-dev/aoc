data = open('./input')

contained_count = 0
overlap_count = 0

def extremes(range):
    x, y = range.split('-')
    return int(x), int(y)

def contained(a, b, c, d):
    return (a >= c and b <= d) or (c >= a and d <= b)

def overlap(a, b, c, d):
    # note: no need to consider fully contained + can overlap on a single section
    return (b > d >= a > c) or (d > b >= c > a)

for line in data:
    range1, range2 = line.strip().split(',')
    a, b = extremes(range1)
    c, d = extremes(range2)
    if contained(a, b, c, d):
        contained_count += 1
        overlap_count += 1  # contained implies overlap
    elif overlap(a, b, c, d):
        overlap_count += 1

print(f'fully contained pairs = {contained_count}')
print(f'overlapping pairs = {overlap_count}')

data.close()