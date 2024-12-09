from collections import namedtuple
from typing import Optional
from copy import deepcopy
from time import time

with open('../inputs/9.txt') as data:
    # it's a single line
    input = data.readline().strip()

###############
# input parsing
###############

begin: float = time()
# create a list of files and free space
disk_map: list[int] = list(map(int, input))
# map it into file id with free space
# contains the file ids
disk: list[Optional[int]] = []
# track blocks with their position and size
Block = namedtuple('Block', ['start_idx', 'size'])
# track the size and position of each file
# in the format id: Block
file_info: dict[int, Block] = {}
# track free space blocks, but this time i am interested
# about their size (format size: [start_idx, ])
free_space: dict[int, list[int]] = {}
total_size: int = 0  # track total size
curr_id: int = 0  # track file id
for i in range(0, len(disk_map), 2):
    # alternate file size and free space
    file_size = disk_map[i]
    for occupied in range(file_size):
        disk.append(curr_id)
    # total size is also the index of the next block
    file_info[curr_id] = Block(total_size, file_size)
    total_size += file_size
    try:
        free_space_size = disk_map[i+1]
    except IndexError:
        # last pair was only file, i reached the end
        break
    else:
        for free in range(free_space_size):
            disk.append(None)
        # the key is the size, useful for part 2
        # the id go in the list starting from the leftmost one
        # only add non-zero size blocks
        if free_space_size != 0:
            if free_space_size in free_space:
                free_space[free_space_size].append(total_size)
            else:
                free_space[free_space_size] = [total_size]
            total_size += free_space_size
        # go to next file
        curr_id += 1

# sanity check
assert total_size == len(disk)
# for part 2
disk2 = deepcopy(disk)
print(f'[input parsing] time: {(time()-begin):.4f}s')

###############
# utils
###############


def compute_checksum(disk: list[Optional[int]]) -> int:
    # compute the checksum sum(file_id*position)
    checksum: int = 0
    for i, num in enumerate(disk):
        if num is not None:  # need to explicitly check because if 0 is also False
            checksum += i * num
        # do not do early exit since in part 2 i can have sparse Nones
    return checksum

###############
# part 1
###############


# replace Nones with file ids starting from the right
# just simulate the whole disk
begin = time()
current_free_block_idx = disk.index(None)
for i, file_id in reversed(list(enumerate(disk))):
    # do not move Nones
    if not file_id:
        continue
    # swap None and file
    disk[current_free_block_idx] = file_id
    disk[i] = None
    # go to next block
    current_free_block_idx = disk.index(None)
    # exit condition: free block index is past
    # the current i
    if current_free_block_idx >= i:
        break

print(f'[part 1] time: {(time()-begin):.4f}s')
# compute checksum
print(f'part 1: {compute_checksum(disk)}')

###############
# part 2
###############

# start from highest file id and try to move the
# whole file, if it fits in a block that is on its left
begin = time()
for file_id in sorted(list(file_info.keys()), reverse=True):
    # look for the leftmost block that can fit the file
    # - filter sizes that can fit (size >= file size)
    # - sort by starting index
    # - if some free space is left, add it back to free blocks
    file_size = file_info[file_id].size
    chosen_size = -1
    block_idx = len(disk2)
    for block_size in free_space:
        if block_size >= file_size:
            # pick leftmost one between the two
            # the list is sorted by id so the first is the leftmost one
            if block_idx > free_space[block_size][0]:
                chosen_size = block_size
                block_idx = free_space[block_size][0]
    if chosen_size == -1 or block_idx > file_info[file_id].start_idx:
        # doesn't fit, don't move block OR
        # fits but it's on the left, skip
        continue
    # move the file, do not need to check nor consolidate the new empty
    # space to the left since it will not be touched by other moves
    for i in range(file_size):
        # assert disk2[block_idx + i] == None  # sanity check
        disk2[block_idx + i] = file_id
        disk2[file_info[file_id].start_idx + i] = None
    # pop the block from the list of free blocks (they are unique)
    free_space[chosen_size].remove(block_idx)
    if free_space[chosen_size] == []:
        # remove key if i run out of blocks
        del free_space[chosen_size]
    # i do need to keep track of the new free block when the file
    # is smaller
    # compute remaining size and add to blocks if necessary
    remaining_size = chosen_size - file_size
    if remaining_size > 0:
        if remaining_size in free_space:
            # append and keep sorted by idx
            free_space[remaining_size].append(block_idx+file_size)
            free_space[remaining_size].sort()
        else:
            # never saw this size, add it
            free_space[remaining_size] = [block_idx+file_size]

print(f'[part 2] time: {(time()-begin):.4f}s')
# compute checksum
print(f'part 2: {compute_checksum(disk2)}')
