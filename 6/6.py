with open('./input') as data:
    input = data.readline().strip()


def find_marker(input, length):
    marker = []
    for i, char in enumerate(input):
        if char not in marker:
            marker.append(char)
            if len(marker) == length:
                offset = i + 1
                break
        else:
            marker = marker[marker.index(char) + 1:]
            marker.append(char)
    return marker, offset


# part 1
start_packet_marker, offset = find_marker(input, 4)
print(f'marker found after {offset} characters: {start_packet_marker}')

# part 2
start_message_marker, offset = find_marker(input, 14)
print(f'marker found after {offset} characters: {start_message_marker}')
