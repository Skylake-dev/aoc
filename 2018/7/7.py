import re
import itertools

with open('./input') as data:
    input = data.readlines()

regex = r'Step ([A-Z]{1}) must be finished before step ([A-Z]{1}) can begin.'

# steps that have been completed
out: str = ''
# all the steps that exist in my problem except final steps
seen: set[str] = set()
# all the steps that have been done
done: set[str] = set()
# dictionary containing all the prerequisites of a certain step
# e.g. {'A': ['B', 'C']} --> steps B and C must be done before A
prerequisites: dict[str, list[str]]  = {}
# dictionary containing all the prerequisites of a certain step
# e.g. {'A': ['B', 'C']} --> after doing A, B and C can come next
possible_followers: dict[str, list[str]]  = {}
# available next states, sorted alphabetically
next_candidates: list[str] = []

# parse input
for line in input:
    # match the two steps
    match = re.match(regex, line)
    assert match is not None
    capture = match.groups()
    before, after = capture
    # keep track of seen states, only if i haven't seen them all
    if len(seen) < 26:
        seen.add(before)
        seen.add(after)
    # keep track of followers
    if before in possible_followers:
        if after not in possible_followers[before]:
            possible_followers[before].append(after)
    else:
        possible_followers[before] = [after]
    # keep track of prerequisites
    if after in prerequisites:
        if before not in prerequisites[after]:
            prerequisites[after].append(before)
    else:
        prerequisites[after] = [before]

# sort all followers alphabetically since we need to go in that order
for k in possible_followers:
    possible_followers[k].sort()

###############
# part 1
###############

# find starting step
not_first = set(itertools.chain(*possible_followers.values()))
possible_steps = set(itertools.chain(*possible_followers.keys()))
# get steps without prerequisites
initial_steps = list(possible_steps.difference(not_first))
# can also find final steps
final_steps = not_first.difference(possible_steps)
seen = seen.difference(final_steps)
# start from first one alphabetically
initial_steps.sort()
out += initial_steps.pop(0)
done.add(out)
# keep track of next states
next_candidates = initial_steps
for el in possible_followers[out]:
    if el not in next_candidates:
        next_candidates.append(el)
# sort the list since i need to
# iterate on next states alphabetically
next_candidates.sort()
# go until i have done all the steps
while(len(seen.difference(done)) != 0):
    # i can safely pop the candidate, if it is not executed
    # it will be put back later when one of its prerequisites finishes
    current_candidate = next_candidates.pop(0)
    if all(x in done for x in prerequisites.get(current_candidate, [])):
        # if all the prerequisites have been satisfied, then
        # append it to the output string
        out += current_candidate
        done.add(current_candidate)
        # add the followers from this new step to the next candidate
        try:
            [next_candidates.append(x) for x in possible_followers[current_candidate] if x not in next_candidates]
        except KeyError:
            # only final states remain
            break
        # keep list sorted alphabetically
        next_candidates.sort()

# add final steps in order
final_steps = list(final_steps)
final_steps.sort()
out += ''.join(final_steps)
print(f'part 1: {out}')

###############
# part 2
###############

# compute the time required by each step
steps = 'QWERTYUIOPASDFGHJKLZXCVBNM'
time_to_completion: dict[str, int] = {}
for s in steps:
    # A is 65 ascii and i need to have 60+alphabet_position
    time_to_completion[s] = ord(s) - 4

# total elapsed time
total_time: int = 0
# number of parallel workers available
WORKERS: int = 5
# how many seconds until the next free worker is available
# stays 0 as long as there is one free worker
next_worker_in: int = 0
# occupied workers
occupied: int = 0
# which steps are being worked on
# there can't be more than WORKERS active tasks
# each tuple is (step, time remaining)
active: list[tuple[str, int]] = []
# initial and final steps are the same
initial_steps = list(possible_steps.difference(not_first))
initial_steps.sort()
final_steps = not_first.difference(possible_steps)
final_steps = list(final_steps)
final_steps.sort()
# start over
done.clear()
next_candidates: list[str] = []

# finds the next completed step from the active queue
# and updates the time remaining
# returns the step that just completed with the time to update
# could use a named tuple
def find_next_completed_and_update() -> tuple[str, int]:
    # find smallest
    timings = [el[1] for el in active]
    minimum = min(timings)
    step_completed = active.pop(timings.index(minimum))
    # update remaining
    for i in range(len(active)):
        active[i] = (active[i][0], active[i][1] - minimum)
    # return step
    return step_completed

# no more than WORKERS possible initials
assert len(initial_steps) <= WORKERS
# start from initials
# since it's sorted we start from first
while initial_steps != []:
    current_initial = initial_steps.pop(0)
    active.append((current_initial, time_to_completion[current_initial]))
    occupied += 1

while(len(seen.difference(done)) != 0):
    step, time = find_next_completed_and_update()
    # update total time and free worker
    total_time += time
    occupied -= 1
    # keep track of completed
    done.add(step)
    # states that possibly become available now
    try:
        [next_candidates.append(x) for x in possible_followers[step] if x not in next_candidates]
    except KeyError:
        # only final states remain, start appending them to the active tasks
        try:
            final = final_steps.pop(0)
        except IndexError:
            # reached the end of final states, exit
            break
        else:
            active.append((final, time_to_completion[final]))
            occupied += 1
    next_candidates.sort()
    # choose next step(s)
    # go until i run out of candidates or workers
    while(len(next_candidates) > 0 and occupied < WORKERS):
        current_candidate = next_candidates.pop(0)
        if all(x in done for x in prerequisites.get(current_candidate, [])):
            active.append((current_candidate, time_to_completion[current_candidate]))
            occupied += 1

# wait for the last ones
while occupied > 0:
    step, time = find_next_completed_and_update()
    total_time += time
    occupied -= 1

print(f'part 2: {total_time}')