numbers = []

with open('./input') as data:
    num = data.readline()
    while num:
        numbers.append(int(num))
        num = data.readline()

new_positions = numbers.copy()

modulus = len(numbers)  # constant


def circular_shift(new_positions, start, end):
    tmp = new_positions[start]
    # print(f'moving {tmp}')
    if end > start:
        sign = 1
        if tmp < 0:
            end -= 1
    else:
        sign = -1
        if tmp > 0:
            end += 1
    while((start - end) % modulus != 0):
        # print(f'start: {start}  end: {end}')
        new_positions[start %
                      modulus] = new_positions[(start + sign) % modulus]
        start = (start + sign) % modulus
    new_positions[end] = tmp


for number in numbers:
    start = new_positions.index(number)
    end = start + number
    if end <= 0:
        end -= 1
    circular_shift(new_positions, start % modulus, end % modulus)
    # print(new_positions)


zero = new_positions.index(0)
offsets = [1000, 2000, 3000]
grove_coords = []
for off in offsets:
    print(
        f'picking {new_positions[(zero+off) % modulus]} at {(zero+off) % modulus}')
    grove_coords.append(new_positions[(zero+off) % modulus])

print(f'grove at {sum(grove_coords)}')
