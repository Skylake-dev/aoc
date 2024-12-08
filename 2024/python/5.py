with open('../inputs/5.txt') as data:
    input = data.readlines()

###############
# input parsing
###############

# similar as 2018 day 7 i keep track of followers
# e.g. {75: [61, 13]} --> 61 and 13 cannot come before 75 (rules 75|61, 75|13)
follower_rules: dict[int, set[int]] = {}
# also track the preceding elements
# e.g. {13: [53, 97]} --> 53 and 97 cannot come before 713 (rules 53|13, 97|13)
preceding_rules: dict[int, set[int]] = {}
# list containing all the lists of pages that need to be changed
updates: list[list[int]] = []

# parse input in two parts, extract the precedence rules
# then get all the list of pages at the end
for i, line in enumerate(input):
    if line == '\n':  # empty lines means start of updates
        # convert each update into a list of ints
        updates = [list(map(int, l.strip().split(','))) for l in input[i+1:]]
        break
    # here parse the ordering rules
    first, second = list(map(int, line.strip().split('|')))
    # track follower
    if first in follower_rules:
        # since it is a set i don't need to worry about duplicates
        follower_rules[first].add(second)
    else:
        follower_rules[first] = set([second])
    # track preceding
    if second in preceding_rules:
        # since it is a set i don't need to worry about duplicates
        preceding_rules[second].add(first)
    else:
        preceding_rules[second] = set([first])


def check_correct(update) -> bool:
    # check that if there are followers rules for this item,
    # that all followers are correct or if there are preceding
    # rules, that all the precedent elements are correct
    for i, page in enumerate(update):
        if ((page in follower_rules and
            any(x not in follower_rules[page] for x in update[i+1:])) or
            (page in preceding_rules and
                any(x not in preceding_rules[page] for x in update[:i]))):
            return False
    return True

###############
# part 1
###############


# keep track of the result
result: int = 0
# also track which ones are correct for part 2
correctness_flags: list[bool] = []
# to check if an update is valid i need to see if it satisfies all
# the priority rules
for update in updates:
    keep: bool = True
    keep = check_correct(update)
    if keep:
        result += update[len(update)//2]
    # keep track of the correctness for part 2
    correctness_flags.append(keep)

print(f'part 1: {result}')

###############
# part 2
###############

# reset result
result: int = 0

for update, correct in zip(updates, correctness_flags):
    # ignore correct update
    if correct:
        continue
    # we have an incorrect update, fix it
    # look for followers violation, then it means that i need to
    # move it before the element that caused the violation
    # for precedence is the same but put the element after
    # repeat until it is correct
    while not correct:
        i = 0
        while i < len(update):
            page = update[i]
            if page in follower_rules:
                for j, follower in enumerate(update[i+1:]):
                    if follower not in follower_rules[page]:
                        # condition violated, move the element before the current one
                        update = update[:i] + [follower] + \
                            update[i:i+j+1] + update[i+j+2:]
                        correct = check_correct(update)
                        i = 0
                        break
            elif page in preceding_rules:
                for j, preceding in enumerate(update[:i]):
                    if preceding not in preceding_rules[page]:
                        # condition violated, move the element after the current one
                        update = update[:j] + update[j+1:i+1] + \
                            [preceding] + update[i+1:]
                        correct = check_correct(update)
                        i = 0
                        break
            if correct:
                break
            i += 1
        if correct:
            # get new middle value
            result += update[len(update)//2]

print(f'part 2: {result}')
